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

    return [
        NewsSourceResponse.model_validate({
            **source.__dict__,
            'article_count': count
        })
        for source, count in sources_with_counts
    ]
