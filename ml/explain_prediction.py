"""
ReviewGuard AI - Prediction Explanation & Feature Attribution
Extracts mathematically grounded TF-IDF token contributions from linear model coefficients
combined with stylistic signals for interpretable, responsible AI explanations.
"""

from typing import Dict, List, Any, Optional
import numpy as np
from ml.preprocess import compute_text_indicators

def extract_influential_terms(
    pipeline: Any,
    raw_text: str,
    top_n: int = 5
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Extracts top words/ngrams that contributed most heavily toward 'Potentially Fake'
    or 'Likely Genuine' based on the fitted TF-IDF weights and classifier coefficients.
    """
    try:
        tfidf = pipeline.named_steps.get("tfidf")
        clf = pipeline.named_steps.get("clf")

        if tfidf is None or clf is None:
            return {"fake_influential": [], "genuine_influential": []}

        # Handle LogisticRegression coefficients
        if hasattr(clf, "coef_"):
            coefs = clf.coef_[0]
        elif hasattr(clf, "calibrated_classifiers_"):
            # CalibratedClassifierCV: average base estimators
            coefs = np.mean([b.estimator.coef_[0] for b in clf.calibrated_classifiers_], axis=0)
        else:
            return {"fake_influential": [], "genuine_influential": []}

        # Vectorize single review
        X_vec = tfidf.transform([raw_text])
        feature_names = np.array(tfidf.get_feature_names_out())

        # Non-zero indices in this document
        row_indices = X_vec.indices
        row_data = X_vec.data

        if len(row_indices) == 0:
            return {"fake_influential": [], "genuine_influential": []}

        # Contribution = tfidf_weight * classifier_weight
        contributions = row_data * coefs[row_indices]
        words = feature_names[row_indices]

        # Sort contributions
        sorted_indices = np.argsort(contributions)

        # Negative contributions push toward Genuine (Class 0)
        genuine_terms = []
        for idx in sorted_indices[:top_n]:
            if contributions[idx] < 0:
                genuine_terms.append({
                    "term": str(words[idx]),
                    "contribution": round(float(contributions[idx]), 4),
                    "impact": "pushes toward Genuine"
                })

        # Positive contributions push toward Fake (Class 1)
        fake_terms = []
        for idx in sorted_indices[::-1][:top_n]:
            if contributions[idx] > 0:
                fake_terms.append({
                    "term": str(words[idx]),
                    "contribution": round(float(contributions[idx]), 4),
                    "impact": "pushes toward Potentially Fake"
                })

        return {
            "fake_influential": fake_terms,
            "genuine_influential": genuine_terms
        }
    except Exception:
        return {"fake_influential": [], "genuine_influential": []}

def build_explanation(
    pipeline: Any,
    raw_text: str,
    predicted_label: int,
    confidence: float
) -> Dict[str, Any]:
    """Synthesizes heuristic stylistic signals with model token attributions."""
    text_stats = compute_text_indicators(raw_text)
    influential_tokens = extract_influential_terms(pipeline, raw_text, top_n=4)

    # Contextual summary
    if predicted_label == 1:
        summary = (
            "The model flagged vocabulary and stylistic structures commonly correlated "
            "with deceptive promotional reviews in benchmark datasets."
        )
    else:
        summary = (
            "The linguistic characteristics align with typical truthful consumer reviews "
            "found in empirical benchmark corpora."
        )

    return {
        "text_indicators": text_stats,
        "signals": text_stats.get("signals", []),
        "influential_terms": influential_tokens,
        "explanation_summary": summary,
        "disclaimer": (
            "ReviewGuard AI provides automated predictions based on learned patterns in review data. "
            "Results are indicative and should not be treated as definitive proof of review fraud."
        )
    }
