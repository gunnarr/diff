"""Text utilities."""
import re


def clean_text(text: str) -> str:
    """Clean and normalize text."""
    if not text:
        return ""

    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove leading/trailing whitespace
    text = text.strip()

    return text


def count_words(text: str) -> int:
    """Count words in text."""
    if not text:
        return 0
    return len(text.split())
