"""
ReviewGuard AI - Pydantic Request & Response Schemas
Provides strict type-checking and OpenAPI documentation for all REST API endpoints.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class ReviewPredictRequest(BaseModel):
    review_text: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="The product review text to be evaluated by the trained ML model."
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "review_text": "We stayed at this hotel last weekend. The room was spacious and clean, though breakfast was a bit crowded."
            }
        }
    }

class TextSignal(BaseModel):
    type: str
    severity: str
    title: str
    description: str

class InfluentialTerm(BaseModel):
    term: str
    contribution: float
    impact: str

class InfluentialTerms(BaseModel):
    fake_influential: List[InfluentialTerm] = []
    genuine_influential: List[InfluentialTerm] = []

class Probabilities(BaseModel):
    genuine: float
    potentially_fake: float

class ReviewPredictResponse(BaseModel):
    prediction: str = Field(..., description="'genuine' or 'potentially_fake'")
    label: int = Field(..., description="0 for genuine, 1 for potentially fake")
    label_name: str
    confidence: float = Field(..., ge=0.0, le=100.0)
    confidence_level: str = Field(..., description="'high', 'medium', or 'low'")
    confidence_text: str
    probabilities: Optional[Probabilities] = None
    model_name: str
    review_length: int
    word_count: int
    signals: List[TextSignal] = []
    influential_terms: InfluentialTerms
    explanation_summary: str
    disclaimer: str

class BatchPredictItem(BaseModel):
    row_id: int
    review_text: str
    status: str
    prediction: str
    label: int
    confidence: float
    confidence_level: Optional[str] = None
    confidence_text: Optional[str] = None
    signals_count: Optional[int] = 0
    error_message: Optional[str] = None

class BatchPredictSummary(BaseModel):
    total_reviews: int
    successful_count: int
    failed_count: int
    genuine_count: int
    fake_count: int
    fake_percentage: float
    avg_confidence: float

class BatchPredictResponse(BaseModel):
    summary: BatchPredictSummary
    results: List[BatchPredictItem]

class ModelInfoResponse(BaseModel):
    model_name: str
    version: str
    training_timestamp: Optional[str] = None
    classes: Dict[str, str]
    dataset_info: Dict[str, Any]
    feature_extraction: Dict[str, Any]
    test_metrics: Dict[str, Any]
    disclaimer: str

class AnalyticsResponse(BaseModel):
    model_name: str
    test_metrics: Dict[str, Any]
    all_models_compared: List[Dict[str, Any]]
    dataset_info: Dict[str, Any]
    confusion_matrix_url: str
    roc_curve_url: str

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    model_name: Optional[str] = None
    version: str
    timestamp: str
