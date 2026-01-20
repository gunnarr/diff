"""DR (Danska public service) scraper."""
from app.scrapers.base import BaseScraper
from typing import List, Optional
import re


class DRScraper(BaseScraper):
    """Scraper for DR Nyheder (Danmarks Radio)."""

    def __init__(self):
        super().__init__('dr')
        self.base_url = 'https://www.dr.dk'

    def get_rss_urls(self) -> List[str]:
        """Return DR RSS feed URLs."""
        return [
            'https://www.dr.dk/nyheder/service/feeds/allenyheder',
            'https://www.dr.dk/nyheder/service/feeds/indland',
            'https://www.dr.dk/nyheder/service/feeds/udland',
        ]

    def get_sitemap_url(self) -> Optional[str]:
        """Return DR sitemap URL."""
        return 'https://www.dr.dk/sitemap.xml'

    def is_article_url(self, url: str) -> bool:
        """Check if URL is a valid DR news article."""
        # DR article URLs typically follow pattern: dr.dk/nyheder/...
        pattern = r'https://www\.dr\.dk/nyheder/.+'
        return bool(re.match(pattern, url))
