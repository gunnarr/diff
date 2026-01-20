"""Manual test script for scraping."""
import asyncio
from app.database import async_session
from app.services.scraper_service import ScraperService
from sqlalchemy import select
from app.models import NewsSource, Article, ArticleVersion


async def test_scrape():
    """Test scraping SVT."""
    async with async_session() as db:
        # Get SVT source
        result = await db.execute(
            select(NewsSource).where(NewsSource.name == "SVT Nyheter")
        )
        source = result.scalar_one()

        print(f"Testing scraping for: {source.name}")
        print(f"Base URL: {source.base_url}")
        print("-" * 50)

        # Run scrape
        service = ScraperService(db)
        result = await service.scrape_source(source.id)

        print(f"\nScraping completed!")
        print(f"Status: {result['status']}")
        print(f"Articles discovered: {result.get('articles_discovered', 0)}")
        print(f"Articles updated: {result.get('articles_updated', 0)}")
        if result.get('errors'):
            print(f"Errors: {result['errors']}")

        # Show some articles
        print("\n" + "=" * 50)
        print("Sample articles:")
        print("=" * 50)

        result = await db.execute(
            select(Article)
            .where(Article.source_id == source.id)
            .limit(5)
        )
        articles = result.scalars().all()

        for article in articles:
            print(f"\n{article.title}")
            print(f"URL: {article.url}")
            print(f"Versions: {article.version_count}")
            print(f"First seen: {article.first_seen_at}")


if __name__ == "__main__":
    print("Starting manual scrape test...")
    asyncio.run(test_scrape())
