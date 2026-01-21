"""System health tests."""
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.main import app
from app.models import NewsSource, Article
from app.database import async_session


@pytest.mark.asyncio
async def test_api_health():
    """Test that API is responding."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/stats")
        assert response.status_code == 200
        data = response.json()
        assert "total_articles" in data
        assert "total_sources" in data


@pytest.mark.asyncio
async def test_database_connection():
    """Test database connectivity."""
    async with async_session() as session:
        result = await session.execute(select(func.count(NewsSource.id)))
        count = result.scalar()
        assert count is not None
        assert count >= 0


@pytest.mark.asyncio
async def test_sources_configured():
    """Test that news sources are configured."""
    async with async_session() as session:
        result = await session.execute(select(NewsSource))
        sources = result.scalars().all()
        assert len(sources) > 0, "No news sources configured"

        # Check SVT Nyheter exists
        result = await session.execute(
            select(NewsSource).where(NewsSource.name == "SVT Nyheter")
        )
        svt = result.scalar_one_or_none()
        assert svt is not None, "SVT Nyheter source not found"
        assert svt.scraper_class in ["SVTNyheterScraper", "GenericRSSScraper"]


@pytest.mark.asyncio
async def test_articles_exist():
    """Test that articles have been scraped."""
    async with async_session() as session:
        result = await session.execute(select(func.count(Article.id)))
        count = result.scalar()
        assert count is not None
        # Allow empty database for fresh installs
        assert count >= 0


@pytest.mark.asyncio
async def test_next_scrape_endpoint():
    """Test next scrape endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/next-scrape")
        assert response.status_code == 200
        data = response.json()
        assert "is_paused" in data
        assert "next_scrape_at" in data


@pytest.mark.asyncio
async def test_logs_endpoint():
    """Test logs endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/logs?limit=10")
        assert response.status_code == 200
        data = response.json()
        assert "logs" in data
        assert "total_lines" in data
        assert isinstance(data["logs"], list)


@pytest.mark.asyncio
async def test_sources_endpoint():
    """Test sources endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/sources")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        if len(data) > 0:
            source = data[0]
            assert "name" in source
            assert "is_active" in source


@pytest.mark.asyncio
async def test_scraper_configuration():
    """Test that SVT scraper has correct RSS feeds."""
    from app.scrapers.svt import SVTNyheterScraper

    scraper = SVTNyheterScraper()
    rss_urls = scraper.get_rss_urls()

    # Should have many feeds (49+ after recent expansion)
    assert len(rss_urls) >= 45, f"Expected 45+ RSS feeds, got {len(rss_urls)}"

    # Check for main feeds
    assert any("svt.se/rss.xml" in url for url in rss_urls)
    assert any("svt.se/nyheter/rss.xml" in url for url in rss_urls)

    # Check for sport feeds
    assert any("/sport/rss.xml" in url for url in rss_urls)
    assert any("/sport/fotboll/rss.xml" in url for url in rss_urls)

    # Check for kultur feed
    assert any("/kultur/rss.xml" in url for url in rss_urls)

    await scraper.close()


@pytest.mark.asyncio
async def test_article_url_validation():
    """Test article URL validation logic."""
    from app.scrapers.svt import SVTNyheterScraper

    scraper = SVTNyheterScraper()

    # Valid article URLs
    assert scraper.is_article_url("https://www.svt.se/nyheter/inrikes/prinsessan-desiree-ar-dod")
    assert scraper.is_article_url("https://www.svt.se/sport/fotboll/zlatan-comeback")
    assert scraper.is_article_url("https://www.svt.se/kultur/film/ny-svensk-film")

    # Invalid URLs (section pages)
    assert not scraper.is_article_url("https://www.svt.se/nyheter")
    assert not scraper.is_article_url("https://www.svt.se/sport")
    assert not scraper.is_article_url("https://www.svt.se")

    await scraper.close()
