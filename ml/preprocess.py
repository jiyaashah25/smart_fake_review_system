"""
ReviewGuard AI - NLP Preprocessing and Feature Extraction
Implements robust text cleaning, normalization, and heuristic indicator extraction
designed for both pipeline integration and interpretable prediction explanations.
"""

import re
import html
import unicodedata
from typing import Dict, List, Any

# Common promotional and superlative trigger phrases
PROMOTIONAL_PATTERNS = [
    r"\bbest\s+(ever|in\s+the\s+world|deal|choice|experience)\b",
    r"\bmust\s+buy\b",
    r"\b100%\s+(recommend|satisfied|genuine|legit)\b",
    r"\bblown\s+away\b",
    r"\bflawless\b",
    r"\bperfection\b",
    r"\blife\s+changing\b",
    r"\bworth\s+every\s+(penny|cent|dollar)\b",
    r"\bhighly\s+recommend\b",
    r"\bdon't\s+hesitate\b",
    r"\bbuy\s+now\b",
    r"\bhurry\b",
    r"\bunbelievable\b",
]

# First person pronouns (often overused in fabricated reviews to project fake personal authority)
PRONOUN_PATTERN = r"\b(i|me|my|mine|myself|we|us|our|ours)\b"

def clean_text(text: Any) -> str:
    """
    Standard text normalization for TF-IDF feature extraction.
    Removes HTML markup, unescapes entities, normalizes unicode,
    and strips redundant whitespace while preserving negation and word meaning.
    """
    if text is None:
        return ""
    
    if not isinstance(text, str):
        text = str(text)

    # Decode HTML entities (e.g. &amp;, &quot;)
    text = html.unescape(text)

    # Strip HTML tags
    text = re.sub(r"<[^>]+>", " ", text)

    # Unicode normalization (NFKD)
    text = unicodedata.normalize("NFKD", text)

    # Normalize excessive repeated characters (e.g., 'amazzzzing' -> 'amazing')
    text = re.sub(r"(.)\1{3,}", r"\1\1", text)

    # Collapse multiple whitespaces
    text = re.sub(r"\s+", " ", text).strip()

    return text

def compute_text_indicators(raw_text: str) -> Dict[str, Any]:
    """
    Computes transparent, interpretable textual indicators from raw review text.
    These are presented to users as supporting qualitative signals, NOT absolute proof.
    """
    if not raw_text or not isinstance(raw_text, str):
        return {
            "char_count": 0,
            "word_count": 0,
            "avg_word_length": 0.0,
            "uppercase_ratio": 0.0,
            "exclamation_count": 0,
            "question_count": 0,
            "repeated_punct_count": 0,
            "pronoun_count": 0,
            "promotional_count": 0,
            "lexical_diversity": 0.0,
            "signals": ["Empty or invalid review text."],
        }

    char_count = len(raw_text)
    words = re.findall(r"\b\w+\b", raw_text)
    word_count = len(words)
    
    avg_word_length = round(sum(len(w) for w in words) / word_count, 2) if word_count > 0 else 0.0

    # Uppercase analysis (excluding whitespaces and punctuation)
    alpha_chars = [c for c in raw_text if c.isalpha()]
    total_alpha = len(alpha_chars)
    uppercase_count = sum(1 for c in alpha_chars if c.isupper())
    uppercase_ratio = round((uppercase_count / total_alpha) * 100, 2) if total_alpha > 0 else 0.0

    # Punctuation counts
    exclamation_count = raw_text.count("!")
    question_count = raw_text.count("?")
    repeated_punct_matches = re.findall(r"([!?.]){2,}", raw_text)
    repeated_punct_count = len(repeated_punct_matches)

    # Pronoun frequency
    pronoun_matches = re.findall(PRONOUN_PATTERN, raw_text, flags=re.IGNORECASE)
    pronoun_count = len(pronoun_matches)

    # Promotional phrase matches
    promotional_count = 0
    matched_promos = []
    for pattern in PROMOTIONAL_PATTERNS:
        matches = re.findall(pattern, raw_text, flags=re.IGNORECASE)
        if matches:
            promotional_count += len(matches)
            matched_promos.append(pattern.replace(r"\b", "").replace(r"\s+", " "))

    # Lexical diversity (unique words / total words)
    unique_words = set(w.lower() for w in words)
    lexical_diversity = round((len(unique_words) / word_count), 2) if word_count > 0 else 0.0

    # Generate human-readable signals
    signals: List[Dict[str, str]] = []

    if word_count < 10 and word_count > 0:
        signals.append({
            "type": "brevity",
            "severity": "medium",
            "title": "Extremely Brief Review",
            "description": f"Contains only {word_count} words; lacks specific descriptive detail."
        })

    if uppercase_ratio > 30.0 and total_alpha > 10:
        signals.append({
            "type": "capitalization",
            "severity": "high",
            "title": "Excessive Capitalization",
            "description": f"{uppercase_ratio:.1f}% uppercase letters detected, commonly associated with spam emphasis."
        })

    if exclamation_count >= 3 or repeated_punct_count >= 2:
        signals.append({
            "type": "punctuation",
            "severity": "medium",
            "title": "Heightened Punctuation Intensity",
            "description": f"Detected {exclamation_count} exclamation points and repeated punctuation sequences."
        })

    if promotional_count > 0:
        signals.append({
            "type": "promotional",
            "severity": "high",
            "title": "Strong Promotional Phrasing",
            "description": f"Contains {promotional_count} high-intensity marketing or superlative phrases."
        })

    if word_count >= 20 and lexical_diversity < 0.60:
        signals.append({
            "type": "repetition",
            "severity": "medium",
            "title": "High Word Repetition",
            "description": f"Low lexical diversity ({lexical_diversity*100:.0f}% unique words), showing repetitive phrasing."
        })

    if pronoun_count >= 5 and word_count > 0 and (pronoun_count / word_count) > 0.15:
        signals.append({
            "type": "pronouns",
            "severity": "low",
            "title": "Elevated First-Person Pronoun Usage",
            "description": "High concentration of self-referential terms (I, me, my, we), common in narrative embellishments."
        })

    if not signals:
        signals.append({
            "type": "natural",
            "severity": "info",
            "title": "Balanced Stylistic Profile",
            "description": "No abnormal punctuation, capitalization, or heavy promotional phrasing patterns detected."
        })

    return {
        "char_count": char_count,
        "word_count": word_count,
        "avg_word_length": avg_word_length,
        "uppercase_ratio": uppercase_ratio,
        "exclamation_count": exclamation_count,
        "question_count": question_count,
        "repeated_punct_count": repeated_punct_count,
        "pronoun_count": pronoun_count,
        "promotional_count": promotional_count,
        "lexical_diversity": lexical_diversity,
        "signals": signals,
    }
