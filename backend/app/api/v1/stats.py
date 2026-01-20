"""Statistics endpoints."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database import get_db
from app.models import Article, ArticleVersion, NewsSource
from pydantic import BaseModel

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
