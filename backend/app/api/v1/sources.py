"""News sources API endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List
from pydantic import BaseModel
from app.api.deps import get_db
from app.models import NewsSource, Article
from app.schemas import NewsSourceResponse
from app.services.scraper_service import ScraperService

router = APIRouter()


class TriggerScrapeResponse(BaseModel):
    """Response for manual scrape trigger."""
    message: str
    source_id: int
    source_name: str


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

    return [
        NewsSourceResponse.model_validate({
            **source.__dict__,
            'article_count': count
        })
        for source, count in sources_with_counts
    ]


@router.post("/sources/{source_id}/scrape", response_model=TriggerScrapeResponse)
async def trigger_scrape(
    source_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Manually trigger a scrape for a specific source."""

    # Get the source
    result = await db.execute(
        select(NewsSource).where(NewsSource.id == source_id)
    )
    source = result.scalar_one_or_none()

    if not source:
        raise HTTPException(status_code=404, detail=f"Source {source_id} not found")

    if not source.is_active:
        raise HTTPException(status_code=400, detail=f"Source {source.name} is not active")

    # Trigger the scrape
    service = ScraperService(db)
    await service.scrape_source(source_id)

    return TriggerScrapeResponse(
        message=f"Scrape triggered for {source.name}",
        source_id=source_id,
        source_name=source.name
    )
