"""News source model."""
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class NewsSource(Base):
    """News source table."""

    __tablename__ = "news_sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    base_url = Column(String(255), nullable=False)
    scraper_class = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    scrape_interval_active = Column(Integer, default=15)  # minutes
    scrape_interval_archive = Column(Integer, default=60)  # minutes
    max_articles_per_scrape = Column(Integer, default=50)
    country = Column(String(50), nullable=True)  # Country code or name
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    articles = relationship("Article", back_populates="source")
