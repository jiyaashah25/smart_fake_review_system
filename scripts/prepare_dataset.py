"""
ReviewGuard AI - Dataset Preparation Pipeline
Loads raw review data, validates schema, applies strict cleaning and label mapping,
and exports the verified dataset to data/processed/cleaned_reviews.csv.
"""

import os
import sys
import json

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from ml.data_loader import (
    load_raw_dataset,
    clean_and_validate_dataset,
    DEFAULT_PROCESSED_PATH,
    DEFAULT_RAW_PATH
)
from scripts.download_dataset import download_dataset

def prepare_dataset():
    print("[INFO] Starting ReviewGuard AI Dataset Preparation...")
    
    if not os.path.exists(DEFAULT_RAW_PATH):
        print(f"[INFO] Raw dataset not found at {DEFAULT_RAW_PATH}. Downloading now...")
        download_dataset()

    raw_df = load_raw_dataset()
    cleaned_df, stats = clean_and_validate_dataset(raw_df)

    os.makedirs(os.path.dirname(DEFAULT_PROCESSED_PATH), exist_ok=True)
    cleaned_df.to_csv(DEFAULT_PROCESSED_PATH, index=False, encoding="utf-8")

    print("[SUCCESS] Dataset cleaned and validated successfully!")
    print(f"[INFO] Processed file saved to: {DEFAULT_PROCESSED_PATH}")
    print("[STATISTICS]")
    print(json.dumps(stats, indent=2))
    
    return cleaned_df, stats

if __name__ == "__main__":
    prepare_dataset()
