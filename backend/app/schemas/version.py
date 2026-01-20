"""Article version schemas."""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ArticleVersionBase(BaseModel):
    """Base article version schema."""
    version_number: int
    title: Optional[str]
    byline: Optional[str]
    content: str
    captured_at: datetime
    word_count: Optional[int]
    published_date: Optional[datetime]
    modified_date: Optional[datetime]


class ArticleVersionResponse(ArticleVersionBase):
    """Article version response schema."""
    id: int
    article_id: int
    content_hash: str
    meta_description: Optional[str]
    meta_keywords: Optional[str]

    class Config:
        from_attributes = True


class ArticleVersionSummary(BaseModel):
    """Compact version info for lists (excludes content for performance)."""
    id: int
    version_number: int
    title: Optional[str]
    captured_at: datetime
    word_count: Optional[int]

    class Config:
        from_attributes = True
