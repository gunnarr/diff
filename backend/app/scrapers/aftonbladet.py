"""Aftonbladet scraper."""
from app.scrapers.base import BaseScraper
from typing import List, Optional
import re


class AftonbladetScraper(BaseScraper):
    """Scraper for Aftonbladet."""

    def __init__(self):
        super().__init__('aftonbladet')
        self.base_url = 'https://www.aftonbladet.se'

    def get_rss_urls(self) -> List[str]:
        """Return Aftonbladet RSS feed URLs."""
        return [
            'https://rss.aftonbladet.se/rss2/small/pages/sections/senastenytt/',
            'https://rss.aftonbladet.se/rss2/small/pages/sections/nyheter/',
            'https://rss.aftonbladet.se/rss2/small/pages/sections/ekonomi/',
        ]

    def get_sitemap_url(self) -> Optional[str]:
        """Return Aftonbladet sitemap URL."""
        return 'https://www.aftonbladet.se/sitemap.xml'

    def is_article_url(self, url: str) -> bool:
        """Check if URL is a valid Aftonbladet news article."""
        # Aftonbladet article URLs typically follow pattern: aftonbladet.se/nyheter/.../a/...
        # Has article ID pattern
        pattern = r'https://www\.aftonbladet\.se/(nyheter|ekonomi|sportbladet)/a/[a-zA-Z0-9]+'
        excluded = r'/(liverapport|bildspel|video)/'
        return bool(re.match(pattern, url)) and not bool(re.search(excluded, url))
