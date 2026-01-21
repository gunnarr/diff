"""Base scraper abstract class."""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict
import asyncio
import re
import httpx
import trafilatura
import feedparser
from bs4 import BeautifulSoup
from datetime import datetime
from app.config import settings


def _clean_text(text: str) -> str:
    """Clean and normalize text."""
    if not text:
        return ""
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove leading/trailing whitespace
    return text.strip()


class BaseScraper(ABC):
    """Abstract base class for all news scrapers."""

    def __init__(self, source_name: str):
        self.source_name = source_name
        self.client = httpx.AsyncClient(
            timeout=30.0,
            headers={
                'User-Agent': settings.USER_AGENT,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'sv-SE,sv;q=0.9,en;q=0.8',
            },
            follow_redirects=True
        )

    @abstractmethod
    def get_rss_urls(self) -> List[str]:
        """Return list of RSS feed URLs for this source."""
        pass

    @abstractmethod
    def get_sitemap_url(self) -> Optional[str]:
        """Return sitemap URL."""
        pass

    @abstractmethod
    def is_article_url(self, url: str) -> bool:
        """Check if URL is an article (vs homepage, section page, etc)."""
        pass

    @staticmethod
    def is_live_article(url: str, title: str = "") -> bool:
        """Check if article is a live/chat article that should be filtered out."""
        url_lower = url.lower()
        title_lower = title.lower()

        # Keywords that indicate live/updating content
        live_keywords = [
            'liverapport', 'direktrapport', 'direkt', 'live',
            'chatt', 'livesändning', 'direktsändning',
            'senaste-nytt', 'senaste_nytt', 'just-nu', 'just_nu',
            'uppdateras', 'följ-med', 'följ_med'
        ]

        # Check URL
        for keyword in live_keywords:
            if keyword in url_lower:
                return True

        # Check title
        for keyword in live_keywords:
            if keyword in title_lower:
                return True

        return False

    async def discover_articles(self, limit: int = 50, concurrent_feeds: int = 8) -> List[str]:
        """Discover article URLs from RSS/sitemap with concurrent feed fetching."""
        urls = []
        feed_urls = self.get_rss_urls()

        # Create semaphore to limit concurrent requests
        semaphore = asyncio.Semaphore(concurrent_feeds)

        async def fetch_feed_with_limit(feed_url: str) -> List[str]:
            async with semaphore:
                try:
                    return await self._parse_rss(feed_url)
                except Exception as e:
                    print(f"Error parsing RSS {feed_url}: {e}")
                    return []

        # Fetch all RSS feeds concurrently (limited by semaphore)
        results = await asyncio.gather(*[fetch_feed_with_limit(url) for url in feed_urls])

        # Flatten results
        for feed_urls_list in results:
            urls.extend(feed_urls_list)

        # Filter to valid article URLs and deduplicate
        urls = list(set([u for u in urls if self.is_article_url(u) and not self.is_live_article(u)]))

        return urls[:limit]

    async def fetch_article(self, url: str) -> Dict:
        """Fetch and extract article content."""
        await asyncio.sleep(1.0)  # Rate limit: 1 second between requests

        try:
            response = await self.client.get(url)
            response.raise_for_status()
            html = response.text

            # Extract content using trafilatura
            content = trafilatura.extract(
                html,
                include_comments=False,
                include_tables=False,
                no_fallback=False,
                favor_recall=True  # Get more content rather than being too strict
            )

            if not content or len(content) < 100:
                # Fallback: try custom extraction
                content = self._custom_extract(html)

            # Extract metadata
            soup = BeautifulSoup(html, 'html.parser')

            title = _clean_text(self._extract_title(soup))

            # Check if this is a live article based on title
            if self.is_live_article(url, title):
                raise ValueError(f"Skipping live/updating article: {title}")

            return {
                'title': title,
                'content': _clean_text(content) if content else "",
                'byline': _clean_text(self._extract_byline(soup)),
                'published_date': self._extract_published_date(soup),
                'modified_date': self._extract_modified_date(soup),
                'meta_description': _clean_text(self._extract_meta_description(soup)),
                'meta_keywords': self._extract_meta_keywords(soup)
            }
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            raise

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract article title."""
        # Try OpenGraph first
        og_title = soup.find('meta', property='og:title')
        if og_title and og_title.get('content'):
            return og_title.get('content', '')

        # Try Twitter card
        twitter_title = soup.find('meta', {'name': 'twitter:title'})
        if twitter_title and twitter_title.get('content'):
            return twitter_title.get('content', '')

        # Fallback to <title>
        title = soup.find('title')
        return title.text.strip() if title else ''

    def _extract_byline(self, soup: BeautifulSoup) -> str:
        """Extract article author/byline."""
        # Try schema.org author markup (itemProp="author") - most accurate for SVT
        authors = []
        author_elements = soup.find_all(attrs={'itemprop': 'author'})
        for elem in author_elements:
            author_text = elem.get_text(strip=True)
            if author_text and author_text not in authors:
                authors.append(author_text)

        if authors:
            # Join multiple authors with "och" for Swedish articles
            if len(authors) == 2:
                return f"{authors[0]} och {authors[1]}"
            elif len(authors) > 2:
                return ", ".join(authors[:-1]) + f" och {authors[-1]}"
            return authors[0]

        # Fallback: Try common author meta tags
        author_meta = soup.find('meta', {'name': 'author'})
        if author_meta and author_meta.get('content'):
            content = author_meta.get('content', '')
            # Skip generic source names like "SVT Nyheter" as they're not actual authors
            if content and content not in ['SVT Nyheter', 'SVT', 'Sveriges Television']:
                return content

        # Try article:author
        article_author = soup.find('meta', property='article:author')
        if article_author and article_author.get('content'):
            return article_author.get('content', '')

        return ''

    def _extract_published_date(self, soup: BeautifulSoup) -> Optional[datetime]:
        """Extract published date."""
        # Try article:published_time
        published = soup.find('meta', property='article:published_time')
        if published and published.get('content'):
            try:
                return datetime.fromisoformat(published['content'].replace('Z', '+00:00'))
            except:
                pass

        return None

    def _extract_modified_date(self, soup: BeautifulSoup) -> Optional[datetime]:
        """Extract modified date."""
        # Try article:modified_time
        modified = soup.find('meta', property='article:modified_time')
        if modified and modified.get('content'):
            try:
                return datetime.fromisoformat(modified['content'].replace('Z', '+00:00'))
            except:
                pass

        return None

    def _extract_meta_description(self, soup: BeautifulSoup) -> str:
        """Extract meta description."""
        desc = soup.find('meta', {'name': 'description'})
        if desc and desc.get('content'):
            return desc.get('content', '')

        og_desc = soup.find('meta', property='og:description')
        if og_desc and og_desc.get('content'):
            return og_desc.get('content', '')

        return ''

    def _extract_meta_keywords(self, soup: BeautifulSoup) -> str:
        """Extract meta keywords."""
        keywords = soup.find('meta', {'name': 'keywords'})
        if keywords and keywords.get('content'):
            return keywords.get('content', '')

        return ''

    def _custom_extract(self, html: str) -> str:
        """Custom content extraction fallback."""
        soup = BeautifulSoup(html, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()

        # Try to find article content
        article = soup.find('article')
        if article:
            return article.get_text(separator=' ', strip=True)

        # Fallback to body
        body = soup.find('body')
        if body:
            return body.get_text(separator=' ', strip=True)

        return ''

    async def _parse_rss(self, feed_url: str) -> List[str]:
        """Parse RSS feed and extract article URLs."""
        await asyncio.sleep(0.5)  # Rate limit: 0.5 seconds between requests

        try:
            response = await self.client.get(feed_url)
            response.raise_for_status()

            feed = feedparser.parse(response.text)
            return [entry.link for entry in feed.entries if hasattr(entry, 'link')]
        except Exception as e:
            print(f"Error parsing RSS {feed_url}: {e}")
            return []

    async def close(self):
        """Close HTTP client."""
        await self.client.aclose()
