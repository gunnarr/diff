"""Article model."""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Article(Base):
    """Article table."""

    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("news_sources.id"), nullable=False)
    url = Column(String(500), unique=True, nullable=False, index=True)
    canonical_url = Column(String(500))
    title = Column(String(500))
    first_seen_at = Column(DateTime(timezone=True), server_default=func.now())
    last_checked_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_modified_at = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)
    check_count = Column(Integer, default=0)
    version_count = Column(Integer, default=0)

    # Relationships
    source = relationship("NewsSource", back_populates="articles")
    versions = relationship(
        "ArticleVersion",
        back_populates="article",
        order_by="desc(ArticleVersion.captured_at)"
    )

    __table_args__ = (
        Index('idx_article_source_active', 'source_id', 'is_active'),
        Index('idx_article_last_checked', 'last_checked_at'),
    )
