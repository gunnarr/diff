"""News source schemas."""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class NewsSourceBase(BaseModel):
    """Base news source schema."""
    name: str
    base_url: str
    scraper_class: str
    is_active: bool
    scrape_interval_active: int
    scrape_interval_archive: int
    max_articles_per_scrape: int
    country: Optional[str] = None


class NewsSourceResponse(NewsSourceBase):
    """News source response schema."""
    id: int
    created_at: datetime
    article_count: Optional[int] = 0

    class Config:
        from_attributes = True
