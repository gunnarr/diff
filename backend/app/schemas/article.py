"""Article schemas."""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from app.schemas.version import ArticleVersionSummary, ArticleVersionResponse
from app.schemas.source import NewsSourceResponse


class ArticleBase(BaseModel):
    """Base article schema."""
    url: str
    title: Optional[str]
    is_active: bool


class ArticleListResponse(ArticleBase):
    """Article list response schema."""
    id: int
    source_id: int
    first_seen_at: datetime
    last_modified_at: Optional[datetime]
    version_count: int
    latest_version: Optional[ArticleVersionSummary] = None

    class Config:
        from_attributes = True


class ArticleDetailResponse(ArticleBase):
    """Article detail response with all versions."""
    id: int
    source_id: int
    canonical_url: Optional[str]
    first_seen_at: datetime
    last_checked_at: Optional[datetime]
    last_modified_at: Optional[datetime]
    check_count: int
    version_count: int
    source: Optional[NewsSourceResponse] = None
    versions: List[ArticleVersionSummary] = []

    class Config:
        from_attributes = True


class PaginatedArticlesResponse(BaseModel):
    """Paginated article list response."""
    total: int
    items: List[ArticleListResponse]
    limit: int
    offset: int
