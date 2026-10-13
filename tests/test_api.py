"""
Integration tests for FastAPI REST API endpoints using TestClient.
"""

import pytest
from starlette.testclient import TestClient
from main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "ReviewGuard AI"
    assert "tagline" in data
    assert data["status"] == "online"

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["model_loaded"] is True
    assert data["model_name"] is not None

def test_model_info_endpoint():
    response = client.get("/api/model-info")
    assert response.status_code == 200
    data = response.json()
    assert "model_name" in data
    assert "classes" in data
    assert "test_metrics" in data
    assert "disclaimer" in data

def test_predict_single_review_success():
    payload = {
        "review_text": "We stayed at this hotel during a family vacation. The staff was courteous and breakfast was decent."
    }
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["prediction"] in ["genuine", "potentially_fake"]
    assert data["label"] in [0, 1]
    assert 0.0 <= data["confidence"] <= 100.0
    assert "signals" in data
    assert "influential_terms" in data
    assert "disclaimer" in data

def test_predict_empty_review_error():
    payload = {"review_text": "   "}
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 400

def test_predict_missing_body():
    response = client.post("/api/predict", json={})
    assert response.status_code == 422

def test_analytics_endpoint():
    response = client.get("/api/analytics")
    assert response.status_code == 200
    data = response.json()
    assert "test_metrics" in data
    assert "all_models_compared" in data
    assert len(data["all_models_compared"]) >= 2
    assert "confusion_matrix_url" in data
    assert "roc_curve_url" in data

def test_visualizations_endpoints():
    cm_res = client.get("/api/visualizations/confusion-matrix")
    assert cm_res.status_code == 200
    assert cm_res.headers["content-type"] == "image/png"

    roc_res = client.get("/api/visualizations/roc-curve")
    assert roc_res.status_code == 200
    assert roc_res.headers["content-type"] == "image/png"
