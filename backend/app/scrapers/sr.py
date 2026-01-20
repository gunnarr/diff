"""Sveriges Radio scraper."""
from app.scrapers.base import BaseScraper
from typing import List, Optional
import re


class SverigesRadioScraper(BaseScraper):
    """Scraper for Sveriges Radio."""

    def __init__(self):
        super().__init__('sr')
        self.base_url = 'https://sverigesradio.se'

    def get_rss_urls(self) -> List[str]:
        """Return SR RSS feed URLs."""
        return [
            'https://api.sr.se/api/rss/program/83',  # Ekot
            'https://api.sr.se/api/rss/program/478',  # Studio Ett
            'https://api.sr.se/api/rss/program/3795',  # Ekonomiekot
        ]

    def get_sitemap_url(self) -> Optional[str]:
        """Return SR sitemap URL."""
        return 'https://sverigesradio.se/sitemap.xml'

    def is_article_url(self, url: str) -> bool:
        """Check if URL is a valid SR news article."""
        # SR article URLs typically follow pattern: sverigesradio.se/artikel/...
        pattern = r'https://(www\.)?sverigesradio\.se/(artikel|sida)/\d+'
        return bool(re.match(pattern, url))
