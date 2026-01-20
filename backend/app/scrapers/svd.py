"""Svenska Dagbladet scraper."""
from app.scrapers.base import BaseScraper
from typing import List, Optional
import re


class SvenskaDagbladetScraper(BaseScraper):
    """Scraper for Svenska Dagbladet."""

    def __init__(self):
        super().__init__('svd')
        self.base_url = 'https://www.svd.se'

    def get_rss_urls(self) -> List[str]:
        """Return SVD RSS feed URLs."""
        return [
            'https://www.svd.se/?service=rss',
            'https://www.svd.se/om/rss',
        ]

    def get_sitemap_url(self) -> Optional[str]:
        """Return SVD sitemap URL."""
        return 'https://www.svd.se/sitemap.xml'

    def is_article_url(self, url: str) -> bool:
        """Check if URL is a valid SVD news article."""
        # SVD article URLs typically have a long alphanumeric ID
        # Pattern: svd.se/a/[alphanumeric-id]/title
        pattern = r'https://www\.svd\.se/a/[a-zA-Z0-9]+/.+'
        return bool(re.match(pattern, url))
