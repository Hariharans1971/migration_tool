"""Deterministic keyword extraction with an optional spaCy model."""
from __future__ import annotations

import re
from collections import Counter

try:
    import spacy

    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        # Installing the spaCy package does not automatically install this model.
        nlp = None
except ImportError:
    # The scraper/report fallback remains usable without the optional NLP stack.
    nlp = None

FALLBACK_STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "in",
    "is", "it", "of", "on", "or", "that", "the", "this", "to", "was", "were",
    "with", "you", "your",
}


def extract_keywords(text: str, limit: int = 5) -> list[str]:
    """Return up to limit keywords in stable frequency order."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if limit < 1:
        raise ValueError("limit must be at least 1")
    if not text.strip():
        return []

    if nlp is not None:
        doc = nlp(text)
        tokens = [
            (token.lemma_ or token.text).lower()
            for token in doc
            if not token.is_stop and not token.is_punct and token.is_alpha
        ]
    else:
        tokens = [
            token.lower()
            for token in re.findall(r"[A-Za-z]+", text)
            if token.lower() not in FALLBACK_STOP_WORDS
        ]

    frequencies = Counter(tokens)
    return [word for word, _ in frequencies.most_common(limit)]
