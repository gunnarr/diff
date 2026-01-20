"""Seed database with initial news sources."""
import asyncio
from app.database import async_session, init_db
from app.models import NewsSource


async def seed_sources():
    """Add initial news sources."""
    await init_db()

    async with async_session() as db:
        # Check if sources already exist
        sources = [
            NewsSource(
                name="SVT Nyheter",
                base_url="https://www.svt.se/nyheter",
                scraper_class="SVTNyheterScraper",
                is_active=True,
                scrape_interval_active=15,
                scrape_interval_archive=60,
                max_articles_per_scrape=50
            ),
            # Add more sources later
        ]

        for source in sources:
            db.add(source)

        await db.commit()
        print("✅ Database seeded with news sources")


if __name__ == "__main__":
    asyncio.run(seed_sources())
