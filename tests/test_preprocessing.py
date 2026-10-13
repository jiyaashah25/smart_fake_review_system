"""
Unit tests for text preprocessing, normalization, and stylistic indicator extraction.
"""

import pytest
from ml.preprocess import clean_text, compute_text_indicators

def test_clean_text_normal():
    raw = "The staff was fantastic and courteous!"
    cleaned = clean_text(raw)
    assert cleaned == "The staff was fantastic and courteous!"

def test_clean_text_empty_and_none():
    assert clean_text("") == ""
    assert clean_text(None) == ""
    assert clean_text("   \n\t   ") == ""

def test_clean_text_html_tags_and_entities():
    raw = "<p>Awesome hotel! &amp; wonderful room &quot;deluxe&quot;.</p>"
    cleaned = clean_text(raw)
    assert "<p>" not in cleaned
    assert "</p>" not in cleaned
    assert "&amp;" not in cleaned
    assert "&" in cleaned
    assert '"deluxe"' in cleaned

def test_clean_text_repeated_characters():
    raw = "Sooooo gooooood service!!!!!"
    cleaned = clean_text(raw)
    # Character repetition capped at 2
    assert "Soo good service!!" in cleaned

def test_clean_text_unicode_normalization():
    raw = "Café au lait and naïve décor"
    cleaned = clean_text(raw)
    assert isinstance(cleaned, str)
    assert len(cleaned) > 0

def test_compute_text_indicators_empty():
    stats = compute_text_indicators("")
    assert stats["word_count"] == 0
    assert stats["char_count"] == 0
    assert len(stats["signals"]) >= 1

def test_compute_text_indicators_promotional_and_punctuation():
    text = "BEST DEAL EVER!!!! Must buy immediately! 100% recommend!"
    stats = compute_text_indicators(text)
    assert stats["exclamation_count"] >= 4
    assert stats["promotional_count"] >= 1
    assert stats["uppercase_ratio"] > 10.0
    signal_titles = [s["title"] for s in stats["signals"]]
    assert any("Promotional" in t for t in signal_titles)
    assert any("Punctuation" in t for t in signal_titles)

def test_compute_text_indicators_brevity():
    text = "Good hotel."
    stats = compute_text_indicators(text)
    assert stats["word_count"] == 2
    signal_titles = [s["title"] for s in stats["signals"]]
    assert any("Brief" in t for t in signal_titles)

def test_compute_text_indicators_balanced():
    text = "We stayed at the hotel for two nights. The location was convenient and the room was quiet and clean."
    stats = compute_text_indicators(text)
    assert stats["word_count"] > 10
    assert stats["exclamation_count"] == 0
    assert stats["promotional_count"] == 0
