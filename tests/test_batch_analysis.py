"""
Integration tests for Batch CSV review upload, validation, parsing and result export structure.
"""

import io
import pytest
from starlette.testclient import TestClient
from main import app

client = TestClient(app)

def test_batch_predict_valid_csv():
    csv_content = (
        "review_text\n"
        "\"The room was clean and check-in was smooth.\"\n"
        "\"BEST DEAL EVER BUY NOW WOW FLALWESS!!!\"\n"
        "\"Great location near the river walk, will come again.\"\n"
    )
    files = {
        "file": ("test_reviews.csv", io.BytesIO(csv_content.encode("utf-8")), "text/csv")
    }

    response = client.post("/api/predict/batch", files=files)
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert "results" in data
    assert data["summary"]["total_reviews"] == 3
    assert data["summary"]["successful_count"] == 3
    assert len(data["results"]) == 3
    assert data["results"][0]["row_id"] == 1
    assert data["results"][0]["prediction"] in ["genuine", "potentially_fake"]

def test_batch_predict_non_csv_rejected():
    files = {
        "file": ("notes.txt", io.BytesIO(b"Some text"), "text/plain")
    }
    response = client.post("/api/predict/batch", files=files)
    assert response.status_code == 400
    assert "Invalid file format" in response.json()["message"]

def test_batch_predict_missing_review_column():
    csv_content = (
        "name,age,city\n"
        "Alice,30,New York\n"
        "Bob,25,Chicago\n"
    )
    files = {
        "file": ("users.csv", io.BytesIO(csv_content.encode("utf-8")), "text/csv")
    }
    response = client.post("/api/predict/batch", files=files)
    assert response.status_code == 400
    assert "missing required column" in response.json()["message"]

def test_batch_predict_empty_csv():
    files = {
        "file": ("empty.csv", io.BytesIO(b""), "text/csv")
    }
    response = client.post("/api/predict/batch", files=files)
    assert response.status_code == 400
