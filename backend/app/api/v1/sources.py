"""News sources API endpoints."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List
from app.api.deps import get_db
from app.models import NewsSource, Article
from app.schemas import NewsSourceResponse

router = APIRouter()


@router.get("/sources", response_model=List[NewsSourceResponse])
async def get_sources(
    db: AsyncSession = Depends(get_db)
):
    """Get all news sources with article counts."""
    result = await db.execute(
        select(
            NewsSource,
            func.count(Article.id).label('article_count')
        )
        .outerjoin(Article)
        .group_by(NewsSource.id)
    )

    sources_with_counts = result.all()

    response = []
    for source, count in sources_with_counts:
        source_dict = {
            'id': source.id,
            'name': source.name,
            'base_url': source.base_url,
            'scraper_class': source.scraper_class,
            'is_active': source.is_active,
            'scrape_interval_active': source.scrape_interval_active,
            'scrape_interval_archive': source.scrape_interval_archive,
            'max_articles_per_scrape': source.max_articles_per_scrape,
            'country': source.country,
            'created_at': source.created_at,
            'article_count': count
        }
        response.append(NewsSourceResponse(**source_dict))

    return response
