"""Add news sources to database."""
import asyncio
from app.database import async_session
from app.models import NewsSource
from sqlalchemy import select


async def add_sources():
    """Add Swedish news sources to database."""
    async with async_session() as db:
        # Check existing sources
        result = await db.execute(select(NewsSource))
        existing = {s.name for s in result.scalars().all()}

        sources_to_add = [
            {
                'name': 'Sveriges Radio',
                'base_url': 'https://sverigesradio.se',
                'scraper_class': 'SverigesRadioScraper',
                'is_active': True,
                'scrape_interval_active': 15,
                'scrape_interval_archive': 60,
                'max_articles_per_scrape': 50
            },
            {
                'name': 'Dagens Nyheter',
                'base_url': 'https://www.dn.se',
                'scraper_class': 'DagensNyheterScraper',
                'is_active': True,
                'scrape_interval_active': 15,
                'scrape_interval_archive': 60,
                'max_articles_per_scrape': 50
            },
            {
                'name': 'Svenska Dagbladet',
                'base_url': 'https://www.svd.se',
                'scraper_class': 'SvenskaDagbladetScraper',
                'is_active': True,
                'scrape_interval_active': 15,
                'scrape_interval_archive': 60,
                'max_articles_per_scrape': 50
            },
            {
                'name': 'Expressen',
                'base_url': 'https://www.expressen.se',
                'scraper_class': 'ExpressenScraper',
                'is_active': True,
                'scrape_interval_active': 15,
                'scrape_interval_archive': 60,
                'max_articles_per_scrape': 50
            },
            {
                'name': 'Aftonbladet',
                'base_url': 'https://www.aftonbladet.se',
                'scraper_class': 'AftonbladetScraper',
                'is_active': True,
                'scrape_interval_active': 15,
                'scrape_interval_archive': 60,
                'max_articles_per_scrape': 50
            }
        ]

        added = 0
        for source_data in sources_to_add:
            if source_data['name'] not in existing:
                source = NewsSource(**source_data)
                db.add(source)
                print(f"✓ Lade till: {source_data['name']}")
                added += 1
            else:
                print(f"○ Finns redan: {source_data['name']}")

        if added > 0:
            await db.commit()
            print(f"\n✓ Totalt {added} nya källor tillagda!")
        else:
            print("\n○ Inga nya källor att lägga till")

        # Show all sources
        result = await db.execute(select(NewsSource))
        all_sources = result.scalars().all()
        print(f"\nAlla källor ({len(all_sources)}):")
        for s in all_sources:
            status = "✓ aktiv" if s.is_active else "○ inaktiv"
            print(f"  - {s.name} ({status}, var {s.scrape_interval_active} min)")


if __name__ == "__main__":
    asyncio.run(add_sources())
