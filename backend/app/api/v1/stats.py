"""Statistics endpoints."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database import get_db
from app.models import Article, ArticleVersion, NewsSource
from app.core.scheduler import scheduler
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

router = APIRouter()


class Stats(BaseModel):
    """System statistics."""
    total_articles: int
    total_versions: int
    articles_with_changes: int
    total_sources: int
    active_sources: int


@router.get("/stats", response_model=Stats)
async def get_stats(db: AsyncSession = Depends(get_db)):
    """Get system statistics."""

    # Total articles
    result = await db.execute(select(func.count(Article.id)))
    total_articles = result.scalar() or 0

    # Total versions
    result = await db.execute(select(func.count(ArticleVersion.id)))
    total_versions = result.scalar() or 0

    # Articles with changes (version_count > 1)
    result = await db.execute(
        select(func.count(Article.id)).where(Article.version_count > 1)
    )
    articles_with_changes = result.scalar() or 0

    # Total sources
    result = await db.execute(select(func.count(NewsSource.id)))
    total_sources = result.scalar() or 0

    # Active sources
    result = await db.execute(
        select(func.count(NewsSource.id)).where(NewsSource.is_active == True)
    )
    active_sources = result.scalar() or 0

    return Stats(
        total_articles=total_articles,
        total_versions=total_versions,
        articles_with_changes=articles_with_changes,
        total_sources=total_sources,
        active_sources=active_sources
    )


class NextScrapeResponse(BaseModel):
    """Next scheduled scrape information."""
    next_scrape_at: Optional[datetime]
    seconds_until_scrape: Optional[int]
    source_name: Optional[str]
    is_paused: bool = False


@router.get("/next-scrape", response_model=NextScrapeResponse)
async def get_next_scrape():
    """Get information about the next scheduled scrape."""

    if not scheduler.running:
        return NextScrapeResponse(
            next_scrape_at=None,
            seconds_until_scrape=None,
            source_name=None,
            is_paused=True
        )

    # Get all scheduled jobs
    jobs = scheduler.get_jobs()

    if not jobs:
        return NextScrapeResponse(
            next_scrape_at=None,
            seconds_until_scrape=None,
            source_name=None,
            is_paused=True
        )

    # Find the job with the earliest next run time
    next_job = min(jobs, key=lambda j: j.next_run_time if j.next_run_time else datetime.max)

    if not next_job.next_run_time:
        return NextScrapeResponse(
            next_scrape_at=None,
            seconds_until_scrape=None,
            source_name=None
        )

    # Calculate seconds until next scrape
    now = datetime.now(next_job.next_run_time.tzinfo)
    seconds_until = int((next_job.next_run_time - now).total_seconds())

    # Extract source name from job id (format: scrape_{source_name}_active)
    source_name = next_job.id.replace('scrape_', '').replace('_active', '').replace('_', ' ').title()

    return NextScrapeResponse(
        next_scrape_at=next_job.next_run_time,
        seconds_until_scrape=max(0, seconds_until),
        source_name=source_name
    )
