"""Scrape log model."""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class ScrapeLog(Base):
    """Scrape log table."""

    __tablename__ = "scrape_logs"

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("news_sources.id"), nullable=False)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    status = Column(String(20))  # "success", "partial", "failed"
    articles_discovered = Column(Integer, default=0)
    articles_updated = Column(Integer, default=0)
    errors = Column(JSON)  # List of error messages

    # Relationships
    source = relationship("NewsSource", back_populates="scrape_logs")

    __table_args__ = (
        Index('idx_scrape_log_source_time', 'source_id', 'started_at'),
    )
