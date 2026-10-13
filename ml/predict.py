"""
ReviewGuard AI - Prediction Inference Engine
Handles single and batch inference with input validation, probability calibration safeguards,
and transparent prediction explainability.
"""

import os
from typing import Dict, Any, List, Optional
import joblib
import numpy as np

from ml.evaluate_model import MODELS_DIR
from ml.explain_prediction import build_explanation

DEFAULT_MODEL_PATH = os.path.join(MODELS_DIR, "fake_review_model.joblib")

_MODEL_CACHE: Optional[Dict[str, Any]] = None

def get_model(model_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Loads and caches the trained model artifact from disk.
    Ensures model is loaded once at startup rather than on every prediction.
    """
    global _MODEL_CACHE
    path = model_path or DEFAULT_MODEL_PATH

    if _MODEL_CACHE is not None and model_path is None:
        return _MODEL_CACHE

    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Trained model artifact not found at: {path}. "
            f"Please run 'python -m ml.train_model' to train and persist the model first."
        )

    try:
        artifact = joblib.load(path)
        if not isinstance(artifact, dict) or "pipeline" not in artifact:
            raise ValueError("Invalid model artifact format: missing 'pipeline' key.")
        
        if model_path is None:
            _MODEL_CACHE = artifact
        return artifact
    except Exception as e:
        raise RuntimeError(f"Failed to load model artifact: {str(e)}")

def clear_model_cache():
    """Clear memory model cache if retraining occurred."""
    global _MODEL_CACHE
    _MODEL_CACHE = None

def predict_review(
    review_text: str,
    model_path: Optional[str] = None,
    max_length: int = 10000
) -> Dict[str, Any]:
    """
    Generates a machine learning classification for a single review.
    Rejects empty or whitespace-only inputs and returns responsible confidence scores.
    """
    if review_text is None:
        raise ValueError("Review text cannot be null.")

    if not isinstance(review_text, str):
        raise TypeError("Review text must be a string.")

    cleaned_input = review_text.strip()
    if not cleaned_input:
        raise ValueError("Review text cannot be empty or solely whitespace.")

    if len(cleaned_input) > max_length:
        raise ValueError(f"Review exceeds maximum allowed length of {max_length} characters.")

    artifact = get_model(model_path)
    pipeline = artifact["pipeline"]
    model_name = artifact.get("model_name", "ReviewGuard Classifier")

    # Run inference through fitted scikit-learn pipeline
    pred_label = int(pipeline.predict([cleaned_input])[0])

    # Extract calibrated confidence/probability if available
    confidence = 50.0
    probabilities = None

    if hasattr(pipeline, "predict_proba"):
        probs = pipeline.predict_proba([cleaned_input])[0]
        # Probability of the predicted class
        pred_prob = float(probs[pred_label])
        confidence = round(pred_prob * 100.0, 2)
        probabilities = {
            "genuine": round(float(probs[0]) * 100.0, 2),
            "potentially_fake": round(float(probs[1]) * 100.0, 2)
        }
    elif hasattr(pipeline, "decision_function"):
        # Linear decision distance
        dist = float(pipeline.decision_function([cleaned_input])[0])
        # Sigmoid heuristic for ranking only
        sig_prob = 1.0 / (1.0 + np.exp(-dist))
        confidence = round(sig_prob * 100.0 if pred_label == 1 else (1 - sig_prob) * 100.0, 2)

    # Categorize confidence responsibly
    if confidence >= 80.0:
        confidence_level = "high"
        confidence_text = f"High confidence ({confidence:.1f}%)"
    elif confidence >= 65.0:
        confidence_level = "medium"
        confidence_text = f"Moderate confidence ({confidence:.1f}%)"
    else:
        confidence_level = "low"
        confidence_text = f"Limited certainty ({confidence:.1f}%)"

    prediction_slug = "potentially_fake" if pred_label == 1 else "genuine"
    label_name = "Potentially Fake Review" if pred_label == 1 else "Likely Genuine Review"

    words = cleaned_input.split()
    char_count = len(cleaned_input)
    word_count = len(words)

    # Build explanation details
    explanation = build_explanation(pipeline, cleaned_input, pred_label, confidence)

    return {
        "prediction": prediction_slug,
        "label": pred_label,
        "label_name": label_name,
        "confidence": confidence,
        "confidence_level": confidence_level,
        "confidence_text": confidence_text,
        "probabilities": probabilities,
        "model_name": model_name,
        "review_length": char_count,
        "word_count": word_count,
        "signals": explanation["signals"],
        "influential_terms": explanation["influential_terms"],
        "explanation_summary": explanation["explanation_summary"],
        "disclaimer": explanation["disclaimer"]
    }

def predict_batch(
    reviews: List[Dict[str, Any]],
    model_path: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Processes a list of review dicts: [{'row_id': 1, 'review_text': '...'}, ...]
    Returns batch predictions with preservation of order and row identifiers.
    """
    results = []
    for item in reviews:
        row_id = item.get("row_id")
        text = item.get("review_text", "")
        
        if not text or not isinstance(text, str) or not text.strip():
            results.append({
                "row_id": row_id,
                "review_text": str(text),
                "status": "error",
                "error_message": "Empty or invalid review text.",
                "prediction": "unknown",
                "label": -1,
                "confidence": 0.0,
            })
            continue

        try:
            pred = predict_review(text, model_path=model_path)
            pred["row_id"] = row_id
            pred["review_text"] = text
            pred["status"] = "success"
            results.append(pred)
        except Exception as e:
            results.append({
                "row_id": row_id,
                "review_text": text,
                "status": "error",
                "error_message": str(e),
                "prediction": "unknown",
                "label": -1,
                "confidence": 0.0,
            })

    return results
