"""Diff API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.services.diff_service import DiffService
from app.schemas import DiffResponse

router = APIRouter()


@router.get("/diff/{article_id}", response_model=DiffResponse)
async def get_article_diff(
    article_id: int,
    from_version: int = Query(..., description="Starting version number"),
    to_version: int = Query(..., description="Ending version number"),
    db: AsyncSession = Depends(get_db)
):
    """Get diff between two versions of an article."""
    try:
        diff_service = DiffService(db)
        diff = await diff_service.generate_diff(article_id, from_version, to_version)
        return diff
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating diff: {str(e)}")
