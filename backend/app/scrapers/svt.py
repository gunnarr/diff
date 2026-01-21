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
        """Return SVT RSS feed URLs including all regions, categories, and sports."""
        # Main news feeds
        feeds = [
            'https://www.svt.se/rss.xml',
            'https://www.svt.se/nyheter/rss.xml',
            'https://www.svt.se/nyheter/inrikes/rss.xml',
            'https://www.svt.se/nyheter/utrikes/rss.xml',
            'https://www.svt.se/nyheter/lokalt/rss.xml',
        ]

        # News category feeds
        news_categories = ['ekonomi', 'vetenskap']
        for category in news_categories:
            feeds.append(f'https://www.svt.se/nyheter/{category}/rss.xml')

        # Culture feed
        feeds.append('https://www.svt.se/kultur/rss.xml')

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

        # Sport feeds - general
        feeds.append('https://www.svt.se/sport/rss.xml')

        # Sport feeds - specific sports
        sports = [
            'alpint', 'bandy', 'basket', 'cykel', 'fotboll', 'friidrott',
            'golf', 'handboll', 'innebandy', 'ishockey', 'konstakning',
            'langdskidor', 'motorsport', 'ridsport', 'simning', 'skidskytte',
            'tennis', 'trav', 'vintersport', 'volleyboll'
        ]
        for sport in sports:
            feeds.append(f'https://www.svt.se/sport/{sport}/rss.xml')

        return feeds

    def get_sitemap_url(self) -> Optional[str]:
        """Return SVT sitemap URL."""
        return 'https://www.svt.se/sitemap.xml'

    def is_article_url(self, url: str) -> bool:
        """Check if URL is a valid SVT article (news, sport, or culture)."""
        # SVT article URLs follow patterns like:
        # - svt.se/nyheter/.../...
        # - svt.se/sport/.../...
        # - svt.se/kultur/.../...
        # But not just section pages like svt.se/nyheter/inrikes
        patterns = [
            r'https://www\.svt\.se/nyheter/[^/]+/.+',
            r'https://www\.svt\.se/sport/[^/]+/.+',
            r'https://www\.svt\.se/kultur/[^/]+/.+'
        ]
        return any(re.match(pattern, url) for pattern in patterns)
