"""Articles API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from typing import Optional
from datetime import datetime
from app.api.deps import get_db
from app.models import Article, ArticleVersion, NewsSource
from app.schemas import (
    ArticleListResponse,
    ArticleDetailResponse,
    PaginatedArticlesResponse,
    ArticleVersionSummary,
    NewsSourceResponse
)
from app.utils.slug import slugify

router = APIRouter()


@router.get("/articles", response_model=PaginatedArticlesResponse)
async def get_articles(
    source: Optional[str] = Query(None, description="Filter by source name"),
    has_changes: Optional[bool] = Query(None, description="Filter articles with multiple versions"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    """Get paginated list of articles."""
    # Build query
    query = select(Article).options()

    # Filter by source if provided
    if source:
        result = await db.execute(
            select(NewsSource).where(NewsSource.name == source)
        )
        news_source = result.scalar_one_or_none()
        if not news_source:
            raise HTTPException(status_code=404, detail=f"Source '{source}' not found")
        query = query.where(Article.source_id == news_source.id)

    # Filter by has_changes
    if has_changes is not None:
        if has_changes:
            query = query.where(Article.version_count > 1)
        else:
            query = query.where(Article.version_count == 1)

    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    # Get articles with pagination
    query = query.order_by(desc(Article.last_modified_at)).limit(limit).offset(offset)
    result = await db.execute(query)
    articles = result.scalars().all()

    # Build response with latest version info
    items = []
    for article in articles:
        # Get latest version
        version_result = await db.execute(
            select(ArticleVersion)
            .where(ArticleVersion.article_id == article.id)
            .order_by(desc(ArticleVersion.version_number))
            .limit(1)
        )
        latest_version = version_result.scalar_one_or_none()

        latest_version_summary = None
        if latest_version:
            latest_version_summary = ArticleVersionSummary(
                id=latest_version.id,
                version_number=latest_version.version_number,
                title=latest_version.title,
                content=latest_version.content,
                captured_at=latest_version.captured_at,
                word_count=latest_version.word_count
            )

        items.append(ArticleListResponse(
            id=article.id,
            source_id=article.source_id,
            url=article.url,
            title=article.title,
            is_active=article.is_active,
            first_seen_at=article.first_seen_at,
            last_modified_at=article.last_modified_at,
            version_count=article.version_count,
            latest_version=latest_version_summary
        ))

    return PaginatedArticlesResponse(
        total=total,
        items=items,
        limit=limit,
        offset=offset
    )


@router.get("/articles/{date}/{slug}", response_model=ArticleDetailResponse)
async def get_article_by_slug(
    date: str,
    slug: str,
    db: AsyncSession = Depends(get_db)
):
    """Get article by date and slug (e.g., /articles/2026-01-20/artikel-titel)."""
    try:
        # Parse date
        article_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    # Find articles from that date
    # Use func.date() which works across different SQL databases
    result = await db.execute(
        select(Article).where(
            func.date(Article.first_seen_at) == article_date
        )
    )
    articles = result.scalars().all()

    # Find matching article by slug
    article = None
    for a in articles:
        if slugify(a.title) == slug:
            article = a
            break

    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    # Get source
    source_result = await db.execute(
        select(NewsSource).where(NewsSource.id == article.source_id)
    )
    source = source_result.scalar_one_or_none()

    # Get all versions
    versions_result = await db.execute(
        select(ArticleVersion)
        .where(ArticleVersion.article_id == article.id)
        .order_by(desc(ArticleVersion.version_number))
    )
    versions = versions_result.scalars().all()

    version_summaries = [
        ArticleVersionSummary(
            id=v.id,
            version_number=v.version_number,
            title=v.title,
            content=v.content,
            captured_at=v.captured_at,
            word_count=v.word_count
        )
        for v in versions
    ]

    source_response = None
    if source:
        source_response = NewsSourceResponse(
            id=source.id,
            name=source.name,
            base_url=source.base_url,
            scraper_class=source.scraper_class,
            is_active=source.is_active,
            scrape_interval_active=source.scrape_interval_active,
            scrape_interval_archive=source.scrape_interval_archive,
            max_articles_per_scrape=source.max_articles_per_scrape,
            created_at=source.created_at,
            article_count=0
        )

    return ArticleDetailResponse(
        id=article.id,
        source_id=article.source_id,
        url=article.url,
        canonical_url=article.canonical_url,
        title=article.title,
        is_active=article.is_active,
        first_seen_at=article.first_seen_at,
        last_checked_at=article.last_checked_at,
        last_modified_at=article.last_modified_at,
        check_count=article.check_count,
        version_count=article.version_count,
        source=source_response,
        versions=version_summaries
    )


@router.get("/articles/{article_id}", response_model=ArticleDetailResponse)
async def get_article(
    article_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get article details with all versions."""
    # Get article
    result = await db.execute(
        select(Article).where(Article.id == article_id)
    )
    article = result.scalar_one_or_none()

    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    # Get source
    source_result = await db.execute(
        select(NewsSource).where(NewsSource.id == article.source_id)
    )
    source = source_result.scalar_one_or_none()

    # Get all versions
    versions_result = await db.execute(
        select(ArticleVersion)
        .where(ArticleVersion.article_id == article_id)
        .order_by(desc(ArticleVersion.version_number))
    )
    versions = versions_result.scalars().all()

    version_summaries = [
        ArticleVersionSummary(
            id=v.id,
            version_number=v.version_number,
            title=v.title,
            content=v.content,
            captured_at=v.captured_at,
            word_count=v.word_count
        )
        for v in versions
    ]

    source_response = None
    if source:
        source_response = NewsSourceResponse(
            id=source.id,
            name=source.name,
            base_url=source.base_url,
            scraper_class=source.scraper_class,
            is_active=source.is_active,
            scrape_interval_active=source.scrape_interval_active,
            scrape_interval_archive=source.scrape_interval_archive,
            max_articles_per_scrape=source.max_articles_per_scrape,
            created_at=source.created_at,
            article_count=0
        )

    return ArticleDetailResponse(
        id=article.id,
        source_id=article.source_id,
        url=article.url,
        canonical_url=article.canonical_url,
        title=article.title,
        is_active=article.is_active,
        first_seen_at=article.first_seen_at,
        last_checked_at=article.last_checked_at,
        last_modified_at=article.last_modified_at,
        check_count=article.check_count,
        version_count=article.version_count,
        source=source_response,
        versions=version_summaries
    )
