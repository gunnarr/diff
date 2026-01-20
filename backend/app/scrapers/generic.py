"""Generic RSS-based scraper for Swedish news sites."""
from app.scrapers.base import BaseScraper
from typing import List, Optional
import re


class GenericRSSScraper(BaseScraper):
    """Generic scraper that works with most Swedish news sites via RSS."""

    def __init__(self, source_name: str, base_url: str):
        super().__init__(source_name)
        self.base_url = base_url
        self._rss_urls = None
        self._sitemap_url = None

    def get_rss_urls(self) -> List[str]:
        """Return common RSS feed URL patterns for Swedish news sites."""
        if self._rss_urls:
            return self._rss_urls

        # Try common RSS URL patterns
        patterns = [
            f'{self.base_url}/rss',
            f'{self.base_url}/rss.xml',
            f'{self.base_url}/feed',
            f'{self.base_url}/feeds/rss',
            f'{self.base_url}/nyheter/rss',
            f'{self.base_url}/senaste/rss',
        ]
        return patterns

    def get_sitemap_url(self) -> Optional[str]:
        """Return sitemap URL."""
        if self._sitemap_url:
            return self._sitemap_url
        return f'{self.base_url}/sitemap.xml'

    def is_article_url(self, url: str) -> bool:
        """Check if URL looks like an article."""
        # Exclude common non-article patterns
        excluded_patterns = [
            r'/kategori/',
            r'/tag/',
            r'/author/',
            r'/sida/',
            r'/page/',
            r'/arkiv/',
            r'/search/',
            r'/sok/',
            r'/(rss|feed|sitemap)',
            r'/video/',
            r'/liverapport/',
            r'/bildspel/',
            r'/galleri/',
        ]

        for pattern in excluded_patterns:
            if re.search(pattern, url, re.IGNORECASE):
                return False

        # Must be from same domain
        domain = self.base_url.replace('https://', '').replace('http://', '')
        if domain not in url:
            return False

        # Should have reasonable depth (not just homepage)
        path = url.replace(self.base_url, '')
        if path.count('/') < 2:
            return False

        return True
