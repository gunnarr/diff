"""Article version model."""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, UniqueConstraint, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class ArticleVersion(Base):
    """Article version table."""

    __tablename__ = "article_versions"

    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey("articles.id"), nullable=False, index=True)
    version_number = Column(Integer, nullable=False)
    title = Column(Text)
    byline = Column(String(255))  # Author
    content = Column(Text, nullable=False)
    content_hash = Column(String(64), nullable=False)  # SHA256
    captured_at = Column(DateTime(timezone=True), server_default=func.now())
    word_count = Column(Integer)

    # Metadata
    meta_description = Column(Text)
    meta_keywords = Column(String(500))
    published_date = Column(DateTime(timezone=True))
    modified_date = Column(DateTime(timezone=True))

    # Relationships
    article = relationship("Article", back_populates="versions")

    __table_args__ = (
        UniqueConstraint('article_id', 'version_number', name='uq_article_version'),
        Index('idx_version_captured', 'captured_at'),
        Index('idx_version_hash', 'content_hash'),
    )
