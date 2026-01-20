"""URL utilities."""
from urllib.parse import urlparse, urlunparse


def normalize_url(url: str) -> str:
    """Normalize URL by removing fragments and sorting query params."""
    parsed = urlparse(url)
    # Remove fragment
    normalized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        parsed.query,
        ''  # Remove fragment
    ))
    return normalized.rstrip('/')
