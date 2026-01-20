"""Hash utilities."""
import hashlib


def content_hash(text: str) -> str:
    """Generate SHA256 hash of text content."""
    return hashlib.sha256(text.encode('utf-8')).hexdigest()
