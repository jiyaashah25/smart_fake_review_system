"""
ReviewGuard AI - REST API Route Handlers
Implements single-review classification, batch CSV analysis, model telemetry, and evaluation analytics.
"""

import os
import io
import json
import csv
import pandas as pd
from typing import List, Dict, Any
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from fastapi.responses import FileResponse

from api.schemas import (
    ReviewPredictRequest,
    ReviewPredictResponse,
    BatchPredictResponse,
    BatchPredictSummary,
    BatchPredictItem,
    ModelInfoResponse,
    AnalyticsResponse
)
from ml.predict import get_model, predict_review, predict_batch
from ml.evaluate_model import MODELS_DIR

router = APIRouter(prefix="/api", tags=["Machine Learning Inference"])

METADATA_FILE = os.path.join(MODELS_DIR, "model_metadata.json")
METRICS_FILE = os.path.join(MODELS_DIR, "model_metrics.json")
COMPARISON_FILE = os.path.join(MODELS_DIR, "model_comparison.csv")
CONFUSION_MATRIX_FILE = os.path.join(MODELS_DIR, "confusion_matrix.png")
ROC_CURVE_FILE = os.path.join(MODELS_DIR, "roc_curve.png")

MAX_BATCH_ROWS = 2000
MAX_UPLOAD_BYTES = 5 * 1024 * 1024  # 5 MB

@router.get("/model-info", response_model=ModelInfoResponse)
def get_model_information():
    """Returns technical metadata, feature representation specs, and test performance metrics."""
    if not os.path.exists(METADATA_FILE):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model metadata artifact not found. Please train the model with 'python -m ml.train_model'."
        )

    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        meta = json.load(f)

    return ModelInfoResponse(
        model_name=meta.get("model_name", "ReviewGuard Classifier"),
        version=meta.get("version", "1.0.0"),
        training_timestamp=meta.get("training_timestamp"),
        classes={"0": "Genuine Review", "1": "Potentially Fake Review"},
        dataset_info=meta.get("dataset_info", {}),
        feature_extraction=meta.get("feature_extraction", {}),
        test_metrics=meta.get("test_metrics", {}),
        disclaimer=meta.get("disclaimer", "")
    )

@router.post("/predict", response_model=ReviewPredictResponse)
def predict_single_review(payload: ReviewPredictRequest):
    """
    Submits a single product or service review to the trained NLP pipeline.
    Returns predicted class, calibrated confidence, stylistic flags, and influential vocabulary.
    """
    cleaned_text = payload.review_text.strip()
    if not cleaned_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Review text cannot be empty or solely whitespace."
        )

    try:
        result = predict_review(cleaned_text)
        return ReviewPredictResponse(**result)
    except FileNotFoundError as fnf:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(fnf))
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Inference error: {str(e)}")

@router.post("/predict/batch", response_model=BatchPredictResponse)
async def predict_batch_reviews(file: UploadFile = File(...)):
    """
    Upload a CSV file containing a 'review_text' column to classify reviews in bulk.
    Validates file format, enforces size limits, and returns per-row predictions plus aggregate stats.
    """
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file format. Only CSV files (.csv) are accepted for batch analysis."
        )

    content = await file.read()
    if len(content) > MAX_UPLOAD_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File size exceeds the 5 MB limit."
        )

    if not content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The uploaded CSV file is empty."
        )

    # Decode CSV
    try:
        decoded_str = content.decode("utf-8")
    except UnicodeDecodeError:
        try:
            decoded_str = content.decode("latin-1")
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unable to decode file. Please ensure the CSV is UTF-8 or standard ASCII encoded."
            )

    # Read CSV using pandas for robust parsing
    try:
        df = pd.read_csv(io.StringIO(decoded_str))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Malformed CSV content: {str(e)}"
        )

    if df.empty:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CSV file contains headers but no data rows."
        )

    if len(df) > MAX_BATCH_ROWS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Batch size limit exceeded. Maximum allowed rows: {MAX_BATCH_ROWS}. (Uploaded: {len(df)})"
        )

    # Find the review text column (case-insensitive check)
    target_col = None
    for col in df.columns:
        if col.strip().lower() in ["review_text", "text", "review", "content", "body"]:
            target_col = col
            break

    if not target_col:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CSV missing required column. Expected 'review_text' (or 'text', 'review')."
        )

    # Prepare review list
    review_items = []
    for idx, raw_val in enumerate(df[target_col].fillna("").astype(str)):
        review_items.append({
            "row_id": idx + 1,
            "review_text": raw_val
        })

    # Execute batch predictions
    predictions = predict_batch(review_items)

    # Compute summary
    total = len(predictions)
    successful = [p for p in predictions if p.get("status") == "success"]
    failed = [p for p in predictions if p.get("status") != "success"]
    
    fake_count = sum(1 for p in successful if p.get("label") == 1)
    genuine_count = sum(1 for p in successful if p.get("label") == 0)
    
    succ_len = len(successful)
    fake_percentage = round((fake_count / succ_len) * 100.0, 2) if succ_len > 0 else 0.0
    avg_confidence = round(sum(p.get("confidence", 0.0) for p in successful) / succ_len, 2) if succ_len > 0 else 0.0

    batch_items = []
    for p in predictions:
        batch_items.append(BatchPredictItem(
            row_id=p["row_id"],
            review_text=p["review_text"],
            status=p["status"],
            prediction=p.get("prediction", "unknown"),
            label=p.get("label", -1),
            confidence=p.get("confidence", 0.0),
            confidence_level=p.get("confidence_level"),
            confidence_text=p.get("confidence_text"),
            signals_count=len(p.get("signals", [])),
            error_message=p.get("error_message")
        ))

    summary = BatchPredictSummary(
        total_reviews=total,
        successful_count=succ_len,
        failed_count=len(failed),
        genuine_count=genuine_count,
        fake_count=fake_count,
        fake_percentage=fake_percentage,
        avg_confidence=avg_confidence
    )

    return BatchPredictResponse(summary=summary, results=batch_items)

@router.get("/analytics", response_model=AnalyticsResponse)
def get_analytics():
    """Loads genuine evaluation metrics and model comparison records generated during model training."""
    if not os.path.exists(METADATA_FILE) or not os.path.exists(METRICS_FILE):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model evaluation artifacts not found. Please run 'python -m ml.train_model'."
        )

    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        meta = json.load(f)

    with open(METRICS_FILE, "r", encoding="utf-8") as f:
        metrics = json.load(f)

    # Load comparison records from CSV if available
    comparison_data = meta.get("all_models_compared", [])
    if os.path.exists(COMPARISON_FILE):
        try:
            comp_df = pd.read_csv(COMPARISON_FILE)
            comparison_data = comp_df.to_dict(orient="records")
        except Exception:
            pass

    return AnalyticsResponse(
        model_name=meta.get("model_name", "Logistic Regression"),
        test_metrics=metrics,
        all_models_compared=comparison_data,
        dataset_info=meta.get("dataset_info", {}),
        confusion_matrix_url="/api/visualizations/confusion-matrix",
        roc_curve_url="/api/visualizations/roc-curve"
    )

@router.get("/visualizations/confusion-matrix")
def get_confusion_matrix_image():
    """Serves the generated confusion matrix heatmap image."""
    if not os.path.exists(CONFUSION_MATRIX_FILE):
        raise HTTPException(status_code=404, detail="Confusion matrix plot not found.")
    return FileResponse(CONFUSION_MATRIX_FILE, media_type="image/png")

@router.get("/visualizations/roc-curve")
def get_roc_curve_image():
    """Serves the generated ROC curve plot image."""
    if not os.path.exists(ROC_CURVE_FILE):
        raise HTTPException(status_code=404, detail="ROC curve plot not found.")
    return FileResponse(ROC_CURVE_FILE, media_type="image/png")
