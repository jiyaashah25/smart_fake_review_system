"""
ReviewGuard AI - Dataset Downloader
Downloads the authoritative Ott et al. Deceptive Opinion Spam benchmark dataset
(ACL 2011 / Cornell NLP: Truthful and Deceptive Opinions).
"""

import os
import sys
import urllib.request
import pandas as pd

RAW_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "raw")
RAW_DATA_PATH = os.path.join(RAW_DATA_DIR, "reviews.csv")

PRIMARY_URL = "https://raw.githubusercontent.com/rajsiddarth/Text_Analytics/master/deceptive-opinion.csv"
FALLBACK_URL = "https://raw.githubusercontent.com/swaroopg92/Fake-Review-Detection/master/deceptive-opinion.csv"

def download_dataset(force: bool = False) -> str:
    """Download the raw dataset if not present or force is True."""
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    
    if os.path.exists(RAW_DATA_PATH) and not force:
        print(f"[INFO] Raw dataset already exists at: {RAW_DATA_PATH}")
        df = pd.read_csv(RAW_DATA_PATH)
        print(f"[INFO] Existing rows: {len(df)}, columns: {list(df.columns)}")
        return RAW_DATA_PATH

    print(f"[INFO] Downloading dataset from primary source: {PRIMARY_URL}")
    for url in [PRIMARY_URL, FALLBACK_URL]:
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ReviewGuard/1.0"}
            )
            with urllib.request.urlopen(req, timeout=15) as response:
                content = response.read().decode("utf-8", errors="replace")
                with open(RAW_DATA_PATH, "w", encoding="utf-8") as f:
                    f.write(content)
            
            df = pd.read_csv(RAW_DATA_PATH)
            print(f"[SUCCESS] Dataset downloaded successfully to: {RAW_DATA_PATH}")
            print(f"[INFO] Total records: {len(df)}, columns: {list(df.columns)}")
            return RAW_DATA_PATH
        except Exception as e:
            print(f"[WARNING] Failed to fetch from {url}: {e}")

    raise RuntimeError(
        "Could not download dataset from any source. "
        "Please check your internet connection or place 'deceptive-opinion.csv' manually as 'data/raw/reviews.csv'."
    )

if __name__ == "__main__":
    download_dataset(force=True)
