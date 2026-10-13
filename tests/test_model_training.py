"""
Unit tests for pipeline building, model training, artifact saving and evaluation metrics.
"""

import os
import joblib
import numpy as np
import pytest
from ml.train_model import build_candidate_pipelines
from ml.evaluate_model import calculate_metrics

def test_candidate_pipelines_instantiation():
    candidates = build_candidate_pipelines()
    assert "Logistic Regression" in candidates
    assert "Multinomial Naive Bayes" in candidates
    assert "Calibrated LinearSVC" in candidates
    for name, pipe in candidates.items():
        assert hasattr(pipe, "fit")
        assert hasattr(pipe, "predict")

def test_pipeline_fit_and_predict_on_fixture():
    candidates = build_candidate_pipelines()
    lr = candidates["Logistic Regression"]
    
    train_texts = [
        "The hotel room was very clean and comfortable.",
        "Staff was attentive and breakfast was tasty.",
        "BEST PRODUCT EVER BUY NOW DISCOUNT CODE AVOID!",
        "100% LIFE CHANGING AMAZING UNBELIEVABLE EXPERIENCE!"
    ]
    train_labels = np.array([0, 0, 1, 1])

    lr.fit(train_texts, train_labels)

    test_text = ["We enjoyed our stay and the beds were soft."]
    pred = lr.predict(test_text)
    assert pred[0] in [0, 1]

def test_calculate_metrics():
    y_true = np.array([0, 1, 0, 1, 1])
    y_pred = np.array([0, 1, 0, 0, 1])
    y_scores = np.array([0.1, 0.9, 0.2, 0.4, 0.8])

    metrics = calculate_metrics(y_true, y_pred, y_scores)
    assert 0.0 <= metrics["accuracy"] <= 1.0
    assert 0.0 <= metrics["precision"] <= 1.0
    assert 0.0 <= metrics["recall"] <= 1.0
    assert 0.0 <= metrics["f1_score"] <= 1.0
    assert metrics["roc_auc"] is not None
    assert metrics["confusion_matrix"]["true_positive"] == 2
    assert metrics["confusion_matrix"]["false_negative"] == 1

def test_saved_artifact_loads_correctly():
    model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "fake_review_model.joblib")
    assert os.path.exists(model_path), "Model artifact should exist"

    artifact = joblib.load(model_path)
    assert "pipeline" in artifact
    assert "model_name" in artifact
    assert "classes" in artifact
    pipeline = artifact["pipeline"]
    preds = pipeline.predict(["The room was nice."])
    assert preds[0] in [0, 1]
