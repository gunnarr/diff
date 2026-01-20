"""Pydantic schemas."""
from app.schemas.source import NewsSourceResponse
from app.schemas.article import (
    ArticleListResponse,
    ArticleDetailResponse,
    PaginatedArticlesResponse
)
from app.schemas.version import ArticleVersionResponse, ArticleVersionSummary
from app.schemas.diff import DiffResponse, DiffChange, DiffStats

__all__ = [
    "NewsSourceResponse",
    "ArticleListResponse",
    "ArticleDetailResponse",
    "PaginatedArticlesResponse",
    "ArticleVersionResponse",
    "ArticleVersionSummary",
    "DiffResponse",
    "DiffChange",
    "DiffStats",
]
