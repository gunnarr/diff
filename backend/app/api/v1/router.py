"""API v1 router."""
from fastapi import APIRouter
from app.api.v1 import sources, articles, diffs, stats

router = APIRouter()

router.include_router(sources.router, tags=["sources"])
router.include_router(articles.router, tags=["articles"])
router.include_router(diffs.router, tags=["diffs"])
router.include_router(stats.router, tags=["stats"])
