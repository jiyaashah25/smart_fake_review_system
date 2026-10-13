"""
Unit tests for data loading, schema normalization, label mapping, and validation.
"""

import os
import pytest
import pandas as pd
from ml.data_loader import clean_and_validate_dataset, load_raw_dataset, load_processed_dataset

def test_clean_and_validate_valid_data():
    raw_df = pd.DataFrame({
        "text": [
            "Had a great stay at the hotel.",
            "Scam product, do not buy!",
            "Had a great stay at the hotel.",  # Duplicate
            "   ",  # Empty
        ],
        "deceptive": ["truthful", "deceptive", "truthful", "truthful"],
        "hotel": ["Hilton", "Marriott", "Hilton", "Hyatt"]
    })

    cleaned_df, stats = clean_and_validate_dataset(raw_df)
    assert len(cleaned_df) == 2
    assert "review_id" in cleaned_df.columns
    assert "review_text" in cleaned_df.columns
    assert "label" in cleaned_df.columns
    assert set(cleaned_df["label"].unique()).issubset({0, 1})
    assert stats["exact_duplicates_removed"] == 1

def test_clean_and_validate_missing_columns():
    bad_df = pd.DataFrame({"random_col": [1, 2, 3]})
    with pytest.raises(ValueError, match="review text column"):
        clean_and_validate_dataset(bad_df)

def test_clean_and_validate_unsupported_labels():
    bad_df = pd.DataFrame({
        "review_text": ["Great place", "Bad place"],
        "label": ["unknown_class", "another_unknown"]
    })
    with pytest.raises(ValueError, match="Unsupported class labels"):
        clean_and_validate_dataset(bad_df)

def test_load_processed_dataset_missing():
    with pytest.raises(FileNotFoundError):
        load_processed_dataset("non_existent_file.csv")

def test_load_real_processed_dataset():
    df = load_processed_dataset()
    assert len(df) > 1000
    assert "review_text" in df.columns
    assert "label" in df.columns
    assert (df["label"] == 0).sum() > 0
    assert (df["label"] == 1).sum() > 0
