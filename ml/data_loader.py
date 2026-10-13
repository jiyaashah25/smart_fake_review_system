"""
ReviewGuard AI - Data Loader & Validation
Handles raw dataset ingestion, column normalization, label mapping (0=Genuine, 1=Potentially Fake),
data hygiene, duplicate removal, and validation statistics.
"""

import os
from typing import Dict, Tuple, Optional
import pandas as pd

DEFAULT_RAW_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "raw", "reviews.csv")
DEFAULT_PROCESSED_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "processed", "cleaned_reviews.csv")

# Standard Label Mapping: 0 = Genuine, 1 = Potentially Fake
LABEL_MAP = {
    # Ott et al. dataset labels
    "truthful": 0,
    "deceptive": 1,
    # Generic string variations
    "genuine": 0,
    "fake": 1,
    "real": 0,
    "spam": 1,
    "legitimate": 0,
    "0": 0,
    "1": 1,
    0: 0,
    1: 1,
}

def load_raw_dataset(raw_path: Optional[str] = None) -> pd.DataFrame:
    """Load raw dataset file from disk."""
    path = raw_path or DEFAULT_RAW_PATH
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Dataset not found at {path}. Please run 'python scripts/download_dataset.py' first."
        )
    df = pd.read_csv(path)
    if df.empty:
        raise ValueError(f"Dataset file at {path} is empty.")
    return df

def clean_and_validate_dataset(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
    """
    Cleans and standardizes raw dataset into the target schema:
    [review_id, review_text, label, product_category, source]
    """
    stats = {
        "raw_rows": len(df),
        "raw_columns": list(df.columns),
    }

    # Normalize column names: lowercase and strip spaces
    normalized_cols = {col: col.strip().lower() for col in df.columns}
    df = df.rename(columns=normalized_cols)

    # Detect text column
    text_col = None
    for candidate in ["review_text", "text", "review", "content", "body"]:
        if candidate in df.columns:
            text_col = candidate
            break
    if not text_col:
        raise ValueError("Could not find a review text column (expected 'review_text', 'text', or 'review').")

    # Detect label column
    label_col = None
    for candidate in ["label", "deceptive", "class", "target", "category"]:
        if candidate in df.columns:
            label_col = candidate
            break
    if not label_col:
        raise ValueError("Could not find a label column (expected 'label', 'deceptive', or 'class').")

    # Extract category and source if available
    category_col = None
    for candidate in ["product_category", "hotel", "category", "product"]:
        if candidate in df.columns:
            category_col = candidate
            break

    source_col = None
    for candidate in ["source", "dataset", "origin"]:
        if candidate in df.columns:
            source_col = candidate
            break

    # Construct standardized dataframe
    cleaned = pd.DataFrame()
    cleaned["review_text"] = df[text_col].astype(str).str.strip()

    # Map labels deterministically
    raw_labels = df[label_col].apply(lambda x: str(x).strip().lower() if not pd.isna(x) else "")
    mapped_labels = raw_labels.map(LABEL_MAP)
    
    # Check for unmapped / invalid labels
    unmapped_mask = mapped_labels.isna()
    if unmapped_mask.any():
        unmapped_values = df.loc[unmapped_mask, label_col].unique()
        raise ValueError(f"Unsupported class labels detected in dataset: {unmapped_values}")

    cleaned["label"] = mapped_labels.astype(int)

    if category_col:
        cleaned["product_category"] = df[category_col].astype(str).str.strip()
    else:
        cleaned["product_category"] = "General"

    if source_col:
        cleaned["source"] = df[source_col].astype(str).str.strip()
    else:
        cleaned["source"] = "Ott et al. Benchmark"

    # Drop null or whitespace-only texts
    cleaned = cleaned[cleaned["review_text"] != ""]
    cleaned = cleaned.dropna(subset=["review_text", "label"])

    stats["rows_after_null_drop"] = len(cleaned)

    # Deduplicate exact review texts
    dup_count = cleaned.duplicated(subset=["review_text"]).sum()
    stats["exact_duplicates_removed"] = int(dup_count)
    cleaned = cleaned.drop_duplicates(subset=["review_text"]).reset_index(drop=True)

    # Generate sequential review_id
    cleaned["review_id"] = [f"rev_{i+1:05d}" for i in range(len(cleaned))]

    # Reorder columns
    cleaned = cleaned[["review_id", "review_text", "label", "product_category", "source"]]

    # Calculate class distribution
    class_counts = cleaned["label"].value_counts().to_dict()
    stats["cleaned_rows"] = len(cleaned)
    stats["class_distribution"] = {
        "genuine_0": int(class_counts.get(0, 0)),
        "potentially_fake_1": int(class_counts.get(1, 0)),
    }
    
    # Imbalance check
    total = len(cleaned)
    if total > 0:
        fake_ratio = stats["class_distribution"]["potentially_fake_1"] / total
        if fake_ratio < 0.05 or fake_ratio > 0.95:
            stats["imbalance_warning"] = f"Extreme class imbalance detected: fake ratio is {fake_ratio:.2%}"

    return cleaned, stats

def load_processed_dataset(processed_path: Optional[str] = None) -> pd.DataFrame:
    """Load cleaned & validated dataset."""
    path = processed_path or DEFAULT_PROCESSED_PATH
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Cleaned dataset not found at {path}. Run 'python scripts/prepare_dataset.py' to generate it."
        )
    df = pd.read_csv(path)
    if df.empty:
        raise ValueError(f"Cleaned dataset at {path} is empty.")
    return df
