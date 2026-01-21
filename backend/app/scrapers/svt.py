"""SVT Nyheter scraper."""
from app.scrapers.base import BaseScraper
from typing import List, Optional
import re


class SVTNyheterScraper(BaseScraper):
    """Scraper for SVT Nyheter (Sveriges Television)."""

    def __init__(self):
        super().__init__('svt')
        self.base_url = 'https://www.svt.se/nyheter'

    def get_rss_urls(self) -> List[str]:
        """Return SVT RSS feed URLs including all local regions."""
        # Main feeds
        feeds = [
            'https://www.svt.se/nyheter/rss.xml',
            'https://www.svt.se/nyheter/inrikes/rss.xml',
            'https://www.svt.se/nyheter/utrikes/rss.xml',
            'https://www.svt.se/nyheter/lokalt/rss.xml',
        ]

        # All local region feeds
        local_regions = [
            'blekinge', 'dalarna', 'gavleborg', 'halland', 'helsingborg',
            'jamtland', 'jonkoping', 'norrbotten', 'orebro', 'ost',
            'skane', 'smaland', 'sodertalje', 'sormland', 'stockholm',
            'uppsala', 'varmland', 'vast', 'vasterbotten', 'vasternorrland',
            'vastmanland'
        ]

        for region in local_regions:
            feeds.append(f'https://www.svt.se/nyheter/lokalt/{region}/rss.xml')

        return feeds

    def get_sitemap_url(self) -> Optional[str]:
        """Return SVT sitemap URL."""
        return 'https://www.svt.se/sitemap.xml'

    def is_article_url(self, url: str) -> bool:
        """Check if URL is a valid SVT news article."""
        # SVT article URLs typically follow pattern: svt.se/nyheter/...
        # But not just section pages like svt.se/nyheter/inrikes
        pattern = r'https://www\.svt\.se/nyheter/[^/]+/.+'
        return bool(re.match(pattern, url))
