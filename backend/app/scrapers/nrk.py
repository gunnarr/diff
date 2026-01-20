"""NRK (Norska public service) scraper."""
from app.scrapers.base import BaseScraper
from typing import List, Optional
import re


class NRKScraper(BaseScraper):
    """Scraper for NRK Nyheter (Norsk Rikskringkasting)."""

    def __init__(self):
        super().__init__('nrk')
        self.base_url = 'https://www.nrk.no'

    def get_rss_urls(self) -> List[str]:
        """Return NRK RSS feed URLs."""
        return [
            'https://www.nrk.no/toppsaker.rss',
            'https://www.nrk.no/nyheter/siste.rss',
            'https://www.nrk.no/urix/toppsaker.rss',
        ]

    def get_sitemap_url(self) -> Optional[str]:
        """Return NRK sitemap URL."""
        return 'https://www.nrk.no/sitemap.xml'

    def is_article_url(self, url: str) -> bool:
        """Check if URL is a valid NRK news article."""
        # NRK article URLs typically follow pattern: nrk.no/nyheter/...
        pattern = r'https://www\.nrk\.no/(nyheter|urix|sport|kultur)/.+'
        return bool(re.match(pattern, url))
