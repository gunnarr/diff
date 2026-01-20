"""URL slug utilities."""
import re
from unicodedata import normalize


def slugify(text: str) -> str:
    """
    Convert text to URL-friendly slug.

    Examples:
        "Så mycket kostar bensin idag" -> "sa-mycket-kostar-bensin-idag"
        "Här är Sveriges största städer!" -> "har-ar-sveriges-storsta-stader"
    """
    if not text:
        return ""

    # Normalize unicode characters
    text = normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')

    # Convert to lowercase
    text = text.lower()

    # Replace Swedish characters before removing
    text = text.replace('å', 'a').replace('ä', 'a').replace('ö', 'o')
    text = text.replace('é', 'e').replace('è', 'e').replace('ü', 'u')

    # Remove non-alphanumeric characters (except spaces and hyphens)
    text = re.sub(r'[^a-z0-9\s-]', '', text)

    # Replace spaces and multiple hyphens with single hyphen
    text = re.sub(r'[\s-]+', '-', text)

    # Remove leading/trailing hyphens
    text = text.strip('-')

    # Limit length
    if len(text) > 100:
        text = text[:100].rsplit('-', 1)[0]

    return text
