"""Scraper service orchestration."""
from datetime import datetime
from typing import List, Dict, Optional
import hashlib
from urllib.parse import urlparse, urlunparse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import NewsSource, Article, ArticleVersion
from app.scrapers import (
    SVTNyheterScraper,
    GenericRSSScraper,
    BaseScraper
)
import logging

logger = logging.getLogger(__name__)


# Inline utility functions
def __content_hash(text: str) -> str:
    """Generate SHA256 hash of text content."""
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def __normalize_url(url: str) -> str:
    """Normalize URL by removing fragments."""
    parsed = urlparse(url)
    normalized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        parsed.query,
        ''  # Remove fragment
    ))
    return normalized.rstrip('/')


def __count_words(text: str) -> int:
    """Count words in text."""
    return len(text.split()) if text else 0


class ScraperService:
    """Service for orchestrating article scraping."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.scraper_registry = {
            'SVTNyheterScraper': SVTNyheterScraper,
            'GenericRSSScraper': GenericRSSScraper,
        }

    def _get_scraper(self, scraper_class: str, source: NewsSource) -> Optional[BaseScraper]:
        """Get scraper instance by class name."""
        scraper_cls = self.scraper_registry.get(scraper_class)
        if scraper_cls:
            # GenericRSSScraper needs source name and base_url
            if scraper_class == 'GenericRSSScraper':
                return scraper_cls(source.name.lower().replace(' ', '_'), source.base_url)
            else:
                return scraper_cls()
        return None

    async def scrape_source(self, source_id: int) -> Dict:
        """Scrape articles for a specific news source."""
        started_at = datetime.utcnow()

        # Get source
        result = await self.db.execute(
            select(NewsSource).where(NewsSource.id == source_id)
        )
        source = result.scalar_one_or_none()

        if not source or not source.is_active:
            logger.info(f"Skipping scrape for source {source_id}: inactive or not found")
            return {'status': 'skipped', 'reason': 'source inactive or not found'}

        logger.info(f"Starting scrape for {source.name}")

        # Get scraper
        scraper = self._get_scraper(source.scraper_class, source)
        if not scraper:
            logger.error(f"Scraper class {source.scraper_class} not found for {source.name}")
            return {'status': 'failed', 'reason': 'scraper not found'}

        articles_discovered = 0
        articles_updated = 0
        errors = []

        try:
            # Discover article URLs
            urls = await scraper.discover_articles(limit=source.max_articles_per_scrape)
            articles_discovered = len(urls)

            logger.info(f"Discovered {articles_discovered} articles for {source.name}")

            # Process each URL
            for url in urls:
                try:
                    await self._process_article(source, scraper, url)
                    articles_updated += 1
                except Exception as e:
                    error_msg = f"Error processing {url}: {str(e)}"
                    logger.error(error_msg)
                    errors.append(error_msg)

            # Calculate scrape duration
            completed_at = datetime.utcnow()
            duration = (completed_at - started_at).total_seconds()
            status = 'success' if not errors else 'partial'

            logger.info(
                f"Completed scrape for {source.name}: "
                f"status={status}, "
                f"duration={duration:.1f}s, "
                f"discovered={articles_discovered}, "
                f"updated={articles_updated}, "
                f"errors={len(errors)}"
            )

            return {
                'status': status,
                'articles_discovered': articles_discovered,
                'articles_updated': articles_updated,
                'errors': len(errors)
            }

        except Exception as e:
            completed_at = datetime.utcnow()
            duration = (completed_at - started_at).total_seconds()
            logger.error(
                f"Fatal error scraping {source.name}: {e} "
                f"(duration={duration:.1f}s)"
            )
            return {'status': 'failed', 'reason': str(e)}

        finally:
            await scraper.close()

    async def _process_article(self, source: NewsSource, scraper: BaseScraper, url: str):
        """Process a single article URL."""
        normalized_url = _normalize_url(url)

        # Check if article exists
        result = await self.db.execute(
            select(Article).where(Article.url == normalized_url)
        )
        article = result.scalar_one_or_none()

        # Fetch article content
        article_data = await scraper.fetch_article(url)

        if not article_data['content']:
            logger.warning(f"No content extracted for {url}")
            return

        # Calculate content hash
        c_hash = _content_hash(article_data['content'])

        # If article doesn't exist, create it
        if not article:
            article = Article(
                source_id=source.id,
                url=normalized_url,
                canonical_url=normalized_url,
                title=article_data['title'],
                first_seen_at=datetime.utcnow(),
                last_checked_at=datetime.utcnow(),
                is_active=True,
                check_count=1,
                version_count=1
            )
            self.db.add(article)
            await self.db.flush()

            # Create first version
            version = ArticleVersion(
                article_id=article.id,
                version_number=1,
                title=article_data['title'],
                byline=article_data['byline'],
                content=article_data['content'],
                _content_hash=c_hash,
                captured_at=datetime.utcnow(),
                word_count=_count_words(article_data['content']),
                meta_description=article_data['meta_description'],
                meta_keywords=article_data['meta_keywords'],
                published_date=article_data['published_date'],
                modified_date=article_data['modified_date']
            )
            self.db.add(version)
            await self.db.commit()

            logger.info(f"New article: {article_data['title'][:50]}...")

        else:
            # Article exists, check if content changed
            article.last_checked_at = datetime.utcnow()
            article.check_count += 1

            # Get latest version
            result = await self.db.execute(
                select(ArticleVersion)
                .where(ArticleVersion.article_id == article.id)
                .order_by(ArticleVersion.version_number.desc())
                .limit(1)
            )
            latest_version = result.scalar_one_or_none()

            # Check if content changed
            if latest_version and latest_version._content_hash != c_hash:
                # Content changed, create new version
                new_version_number = latest_version.version_number + 1
                article.version_count = new_version_number
                article.last_modified_at = datetime.utcnow()
                article.title = article_data['title']

                version = ArticleVersion(
                    article_id=article.id,
                    version_number=new_version_number,
                    title=article_data['title'],
                    byline=article_data['byline'],
                    content=article_data['content'],
                    _content_hash=c_hash,
                    captured_at=datetime.utcnow(),
                    word_count=_count_words(article_data['content']),
                    meta_description=article_data['meta_description'],
                    meta_keywords=article_data['meta_keywords'],
                    published_date=article_data['published_date'],
                    modified_date=article_data['modified_date']
                )
                self.db.add(version)
                await self.db.commit()

                logger.info(f"Updated article (v{new_version_number}): {article_data['title'][:50]}...")
            else:
                # No change
                await self.db.commit()
