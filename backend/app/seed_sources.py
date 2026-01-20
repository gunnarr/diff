"""Auto-seed database with working news sources on startup."""
import asyncio
from sqlalchemy import select
from app.database import async_session
from app.models import NewsSource


WORKING_SOURCES = [
    {
        'name': 'SVT Nyheter',
        'base_url': 'https://www.svt.se/nyheter',
        'scraper_class': 'SVTNyheterScraper',
        'is_active': True,
        'scrape_interval_active': 15,
        'scrape_interval_archive': 60,
        'max_articles_per_scrape': 50,
        'country': 'SE'
    },
    {
        'name': 'NRK Nyheter',
        'base_url': 'https://www.nrk.no/nyheter',
        'scraper_class': 'NRKNyheterScraper',
        'is_active': True,
        'scrape_interval_active': 15,
        'scrape_interval_archive': 60,
        'max_articles_per_scrape': 50,
        'country': 'NO'
    },
    {
        'name': 'DR Nyheder',
        'base_url': 'https://www.dr.dk/nyheder',
        'scraper_class': 'DRNyhederScraper',
        'is_active': True,
        'scrape_interval_active': 15,
        'scrape_interval_archive': 60,
        'max_articles_per_scrape': 50,
        'country': 'DK'
    },
    {
        'name': 'Aftonbladet',
        'base_url': 'https://www.aftonbladet.se',
        'scraper_class': 'AftonbladetScraper',
        'is_active': True,
        'scrape_interval_active': 15,
        'scrape_interval_archive': 60,
        'max_articles_per_scrape': 50,
        'country': 'SE'
    },
    {
        'name': 'Sveriges Radio',
        'base_url': 'https://sverigesradio.se/nyheter',
        'scraper_class': 'SverigesRadioScraper',
        'is_active': True,
        'scrape_interval_active': 15,
        'scrape_interval_archive': 60,
        'max_articles_per_scrape': 50,
        'country': 'SE'
    },
    {
        'name': 'Göteborgs-Posten',
        'base_url': 'https://www.gp.se',
        'scraper_class': 'GenericRSSScraper',
        'is_active': True,
        'scrape_interval_active': 15,
        'scrape_interval_archive': 60,
        'max_articles_per_scrape': 50,
        'country': 'SE'
    },
    {
        'name': 'Svenska Dagbladet',
        'base_url': 'https://www.svd.se',
        'scraper_class': 'SvDScraper',
        'is_active': True,
        'scrape_interval_active': 15,
        'scrape_interval_archive': 60,
        'max_articles_per_scrape': 50,
        'country': 'SE'
    },
]


async def seed_sources_if_empty():
    """Seed database with news sources if empty."""
    async with async_session() as db:
        # Check if sources already exist
        result = await db.execute(select(NewsSource))
        existing_sources = result.scalars().all()
        
        if len(existing_sources) > 0:
            print(f"✓ Database already has {len(existing_sources)} sources, skipping seed")
            return
        
        print("🌱 Database is empty, seeding with working news sources...")
        
        for source_data in WORKING_SOURCES:
            source = NewsSource(**source_data)
            db.add(source)
            print(f"  ✓ Added: {source_data['name']}")
        
        await db.commit()
        print(f"✅ Successfully seeded {len(WORKING_SOURCES)} news sources!")


def seed_sources_sync():
    """Synchronous wrapper for seeding."""
    asyncio.run(seed_sources_if_empty())
