"""
Unit tests for model prediction inference and confidence calibration safeguards.
"""

import pytest
from ml.predict import predict_review

def test_predict_review_valid_input():
    review = "We stayed here for 3 days. The location is near downtown and room was comfortable."
    result = predict_review(review)

    assert result["prediction"] in ["genuine", "potentially_fake"]
    assert result["label"] in [0, 1]
    assert isinstance(result["confidence"], float)
    assert 0.0 <= result["confidence"] <= 100.0
    assert result["confidence_level"] in ["high", "medium", "low"]
    assert result["review_length"] == len(review)
    assert result["word_count"] > 0
    assert "disclaimer" in result
    assert isinstance(result["signals"], list)

def test_predict_review_promotional_style():
    review = "THIS IS THE BEST HOTEL IN THE ENTIRE WORLD!!!! BUY NOW AND BOOK FAST!!!! 100% UNBELIEVABLE!!!!"
    result = predict_review(review)
    assert result["label"] in [0, 1]
    assert result["word_count"] > 5
    # Should detect stylistic flags
    assert len(result["signals"]) >= 1

def test_predict_review_empty_raises_value_error():
    with pytest.raises(ValueError):
        predict_review("")

def test_predict_review_whitespace_only_raises_value_error():
    with pytest.raises(ValueError):
        predict_review("   \n\t   ")

def test_predict_review_exceeds_max_length():
    with pytest.raises(ValueError, match="maximum allowed length"):
        predict_review("abc " * 3000, max_length=50)

def test_predict_review_unicode_and_punctuation():
    review = "L'hôtel était très charmant, café délicieux, et l'accueil chaleureux..."
    result = predict_review(review)
    assert result["prediction"] in ["genuine", "potentially_fake"]
