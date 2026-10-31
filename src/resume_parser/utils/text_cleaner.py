"""Utilities for normalizing text extracted from documents."""

import re
import unicodedata


def clean_text(text: str) -> str:
    """Normalize Unicode and whitespace while preserving paragraph breaks."""
    normalized = unicodedata.normalize("NFKC", text).replace("\x00", "")
    lines = [re.sub(r"[^\S\r\n]+", " ", line).strip() for line in normalized.splitlines()]
    cleaned = "\n".join(lines)
    return re.sub(r"\n{3,}", "\n\n", cleaned).strip()