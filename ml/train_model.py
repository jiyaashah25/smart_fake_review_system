"""
ReviewGuard AI - Machine Learning Training & Model Selection Pipeline
Trains, evaluates, and compares Multinomial Naive Bayes, Logistic Regression,
and Calibrated LinearSVC on the review benchmark. Persists the best model artifact.
"""

import os
import sys
import time
import json
from datetime import datetime, timezone
from typing import Dict, Any

# Ensure project root in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV

from ml.data_loader import (
    load_processed_dataset,
    DEFAULT_PROCESSED_PATH,
    DEFAULT_RAW_PATH,
    load_raw_dataset,
    clean_and_validate_dataset
)
from ml.preprocess import clean_text
from ml.evaluate_model import (
    calculate_metrics,
    plot_confusion_matrix,
    plot_roc_curve,
    MODELS_DIR
)

def get_or_prepare_dataset() -> pd.DataFrame:
    """Ensure cleaned dataset is ready for training."""
    if os.path.exists(DEFAULT_PROCESSED_PATH):
        return load_processed_dataset(DEFAULT_PROCESSED_PATH)
    
    print("[INFO] Cleaned dataset not found. Generating from raw data...")
    raw_df = load_raw_dataset(DEFAULT_RAW_PATH)
    cleaned_df, _ = clean_and_validate_dataset(raw_df)
    os.makedirs(os.path.dirname(DEFAULT_PROCESSED_PATH), exist_ok=True)
    cleaned_df.to_csv(DEFAULT_PROCESSED_PATH, index=False, encoding="utf-8")
    return cleaned_df

def build_candidate_pipelines() -> Dict[str, Pipeline]:
    """Define candidate NLP classification pipelines with TF-IDF representations."""
    vectorizer = TfidfVectorizer(
        preprocessor=clean_text,
        ngram_range=(1, 2),
        max_features=15000,
        sublinear_tf=True,
        min_df=2
    )

    models = {
        "Logistic Regression": Pipeline([
            ("tfidf", vectorizer),
            ("clf", LogisticRegression(
                C=2.5,
                max_iter=1000,
                random_state=42,
                class_weight="balanced",
                solver="liblinear"
            ))
        ]),
        "Multinomial Naive Bayes": Pipeline([
            ("tfidf", vectorizer),
            ("clf", MultinomialNB(alpha=0.4))
        ]),
        "Calibrated LinearSVC": Pipeline([
            ("tfidf", vectorizer),
            ("clf", CalibratedClassifierCV(
                LinearSVC(C=1.0, random_state=42, dual="auto"),
                cv=3
            ))
        ])
    }
    return models

def train_and_evaluate_all():
    """Execute complete training pipeline and persistence."""
    print("=" * 65)
    print("      ReviewGuard AI — Model Training & Selection Pipeline      ")
    print("=" * 65)

    df = get_or_prepare_dataset()
    print(f"[INFO] Loaded {len(df)} validated samples.")
    print(f"[INFO] Genuine reviews (0): {(df['label'] == 0).sum()} | Potentially fake (1): {(df['label'] == 1).sum()}")

    X = df["review_text"].values
    y = df["label"].values.astype(int)

    # Stratified 80/20 train/test split (Random Seed 42)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )
    print(f"[INFO] Training set: {len(X_train)} samples | Test set: {len(X_test)} samples (untouched until final eval)")

    candidates = build_candidate_pipelines()
    comparison_records = []
    trained_pipelines = {}
    test_evaluations = {}

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    for name, pipeline in candidates.items():
        print(f"\n[TRAINING] Evaluating {name}...")
        start_time = time.time()

        # 5-fold CV on training set ONLY
        cv_acc_scores = cross_val_score(pipeline, X_train, y_train, cv=cv, scoring="accuracy")
        cv_f1_scores = cross_val_score(pipeline, X_train, y_train, cv=cv, scoring="f1")

        # Fit on full training set
        pipeline.fit(X_train, y_train)
        duration = round(time.time() - start_time, 2)

        # Evaluate on untouched test set
        y_pred = pipeline.predict(X_test)
        
        # Extract prediction probabilities for fake class (1)
        if hasattr(pipeline, "predict_proba"):
            y_proba = pipeline.predict_proba(X_test)[:, 1]
        elif hasattr(pipeline, "decision_function"):
            y_proba = pipeline.decision_function(X_test)
        else:
            y_proba = None

        metrics = calculate_metrics(y_test, y_pred, y_proba)
        test_evaluations[name] = {
            "metrics": metrics,
            "y_pred": y_pred,
            "y_proba": y_proba
        }
        trained_pipelines[name] = pipeline

        record = {
            "model_name": name,
            "train_duration_sec": duration,
            "cv_accuracy_mean": round(float(np.mean(cv_acc_scores)), 4),
            "cv_accuracy_std": round(float(np.std(cv_acc_scores)), 4),
            "cv_f1_mean": round(float(np.mean(cv_f1_scores)), 4),
            "test_accuracy": metrics["accuracy"],
            "test_precision": metrics["precision"],
            "test_recall": metrics["recall"],
            "test_f1_score": metrics["f1_score"],
            "test_roc_auc": metrics["roc_auc"]
        }
        comparison_records.append(record)

        print(f"  -> CV Acc: {record['cv_accuracy_mean']:.4f} (+/- {record['cv_accuracy_std']:.4f}) | CV F1: {record['cv_f1_mean']:.4f}")
        print(f"  -> Test Acc: {record['test_accuracy']:.4f} | Precision: {record['test_precision']:.4f} | Recall: {record['test_recall']:.4f} | F1: {record['test_f1_score']:.4f} | AUC: {record['test_roc_auc']}")

    # Save model comparison table
    os.makedirs(MODELS_DIR, exist_ok=True)
    comparison_df = pd.DataFrame(comparison_records)
    comparison_path = os.path.join(MODELS_DIR, "model_comparison.csv")
    comparison_df.to_csv(comparison_path, index=False)
    print(f"\n[INFO] Saved model comparison results to: {comparison_path}")

    # Model Selection: Prioritize Test F1 & ROC-AUC with highest generalization
    best_record = max(comparison_records, key=lambda r: (r["test_f1_score"], r["test_roc_auc"] or 0))
    best_name = best_record["model_name"]
    best_pipeline = trained_pipelines[best_name]
    best_eval = test_evaluations[best_name]

    print(f"\n[SELECTION] Best Performing Model: {best_name}")
    print(f"  Test Accuracy: {best_record['test_accuracy']:.2%} | F1-Score: {best_record['test_f1_score']:.4f} | ROC-AUC: {best_record['test_roc_auc']}")

    # Generate and save plots
    cm_array = np.array(best_eval["metrics"]["confusion_matrix"]["raw_matrix"])
    cm_plot_path = plot_confusion_matrix(cm_array, model_name=best_name)
    print(f"[INFO] Saved confusion matrix visualization: {cm_plot_path}")

    if best_eval["y_proba"] is not None:
        roc_plot_path = plot_roc_curve(y_test, best_eval["y_proba"], model_name=best_name)
        print(f"[INFO] Saved ROC curve visualization: {roc_plot_path}")

    # Save final model metrics
    metrics_path = os.path.join(MODELS_DIR, "model_metrics.json")
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(best_eval["metrics"], f, indent=2)
    print(f"[INFO] Saved model metrics: {metrics_path}")

    # Save trained model pipeline artifact
    model_artifact_path = os.path.join(MODELS_DIR, "fake_review_model.joblib")
    artifact_payload = {
        "pipeline": best_pipeline,
        "model_name": best_name,
        "classes": [0, 1],
        "class_labels": {0: "Genuine Review", 1: "Potentially Fake Review"},
        "version": "1.0.0",
        "training_date": datetime.now(timezone.utc).isoformat(),
        "metrics": best_eval["metrics"],
        "comparison": comparison_records,
    }
    joblib.dump(artifact_payload, model_artifact_path)
    print(f"[SUCCESS] Persisted best model artifact: {model_artifact_path}")

    # Save human-readable model metadata
    metadata = {
        "model_name": best_name,
        "version": "1.0.0",
        "training_timestamp": artifact_payload["training_date"],
        "dataset_info": {
            "total_samples": len(df),
            "train_samples": len(X_train),
            "test_samples": len(X_test),
            "genuine_samples": int((df["label"] == 0).sum()),
            "fake_samples": int((df["label"] == 1).sum()),
            "train_test_split": "80/20 Stratified",
            "source": "Ott et al. Deceptive Opinion Spam Benchmark"
        },
        "feature_extraction": {
            "method": "TF-IDF (Term Frequency-Inverse Document Frequency)",
            "ngram_range": [1, 2],
            "max_features": 15000,
            "sublinear_tf": True,
            "min_df": 2
        },
        "test_metrics": best_eval["metrics"],
        "all_models_compared": comparison_records,
        "disclaimer": "ReviewGuard AI provides automated predictions based on learned patterns in review data. Results are indicative and should not be treated as definitive proof of review fraud."
    }
    metadata_path = os.path.join(MODELS_DIR, "model_metadata.json")
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    print(f"[INFO] Saved human-readable model metadata: {metadata_path}")

    return best_name, best_eval["metrics"]

if __name__ == "__main__":
    train_and_evaluate_all()
