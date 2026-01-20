"""Add major Swedish news sources."""
import asyncio
from app.database import async_session
from app.models import NewsSource
from sqlalchemy import select


async def add_major_sources():
    """Add 25+ major Swedish news sources."""
    async with async_session() as db:
        # Check existing sources
        result = await db.execute(select(NewsSource))
        existing = {s.name for s in result.scalars().all()}

        sources_to_add = [
            # National newspapers
            {
                'name': 'Göteborgs-Posten',
                'base_url': 'https://www.gp.se',
                'scraper_class': 'GenericRSSScraper',
                'is_active': True,
                'scrape_interval_active': 15,
                'scrape_interval_archive': 60,
                'max_articles_per_scrape': 50
            },
            {
                'name': 'Sydsvenskan',
                'base_url': 'https://www.sydsvenskan.se',
                'scraper_class': 'GenericRSSScraper',
                'is_active': True,
                'scrape_interval_active': 15,
                'scrape_interval_archive': 60,
                'max_articles_per_scrape': 50
            },
            # Business news
            {
                'name': 'Dagens Industri',
                'base_url': 'https://www.di.se',
                'scraper_class': 'GenericRSSScraper',
                'is_active': True,
                'scrape_interval_active': 15,
                'scrape_interval_archive': 60,
                'max_articles_per_scrape': 50
            },
            {
                'name': 'Affärsvärlden',
                'base_url': 'https://www.affarsvarlden.se',
                'scraper_class': 'GenericRSSScraper',
                'is_active': True,
                'scrape_interval_active': 15,
                'scrape_interval_archive': 60,
                'max_articles_per_scrape': 50
            },
            # News aggregators
            {
                'name': 'Omni',
                'base_url': 'https://omni.se',
                'scraper_class': 'GenericRSSScraper',
                'is_active': True,
                'scrape_interval_active': 15,
                'scrape_interval_archive': 60,
                'max_articles_per_scrape': 50
            },
            # Regional - major
            {
                'name': 'Kvällsposten',
                'base_url': 'https://www.expressen.se/kvallsposten',
                'scraper_class': 'GenericRSSScraper',
                'is_active': True,
                'scrape_interval_active': 15,
                'scrape_interval_archive': 60,
                'max_articles_per_scrape': 50
            },
            {
                'name': 'GT',
                'base_url': 'https://www.expressen.se/gt',
                'scraper_class': 'GenericRSSScraper',
                'is_active': True,
                'scrape_interval_active': 15,
                'scrape_interval_archive': 60,
                'max_articles_per_scrape': 50
            },
            {
                'name': 'Hallandsposten',
                'base_url': 'https://www.hd.se',
                'scraper_class': 'GenericRSSScraper',
                'is_active': True,
                'scrape_interval_active': 20,
                'scrape_interval_archive': 60,
                'max_articles_per_scrape': 30
            },
            {
                'name': 'Helsingborgs Dagblad',
                'base_url': 'https://www.hd.se/helsingborg',
                'scraper_class': 'GenericRSSScraper',
                'is_active': True,
                'scrape_interval_active': 20,
                'scrape_interval_archive': 60,
                'max_articles_per_scrape': 30
            },
            {
                'name': 'Norrköpings Tidningar',
                'base_url': 'https://www.nt.se',
                'scraper_class': 'GenericRSSScraper',
                'is_active': True,
                'scrape_interval_active': 20,
                'scrape_interval_archive': 60,
                'max_articles_per_scrape': 30
            },
            {
                'name': 'Östgöta Correspondenten',
                'base_url': 'https://www.corren.se',
                'scraper_class': 'GenericRSSScraper',
                'is_active': True,
                'scrape_interval_active': 20,
                'scrape_interval_archive': 60,
                'max_articles_per_scrape': 30
            },
            {
                'name': 'Nerikes Allehanda',
                'base_url': 'https://www.na.se',
                'scraper_class': 'GenericRSSScraper',
                'is_active': True,
                'scrape_interval_active': 20,
                'scrape_interval_archive': 60,
                'max_articles_per_scrape': 30
            },
            {
                'name': 'Vestmanlands Läns Tidning',
                'base_url': 'https://www.vlt.se',
                'scraper_class': 'GenericRSSScraper',
                'is_active': True,
                'scrape_interval_active': 20,
                'scrape_interval_archive': 60,
                'max_articles_per_scrape': 30
            },
            {
                'name': 'Dala-Demokraten',
                'base_url': 'https://www.dalademokraten.se',
                'scraper_class': 'GenericRSSScraper',
                'is_active': True,
                'scrape_interval_active': 20,
                'scrape_interval_archive': 60,
                'max_articles_per_scrape': 30
            },
            {
                'name': 'Gefle Dagblad',
                'base_url': 'https://www.gd.se',
                'scraper_class': 'GenericRSSScraper',
                'is_active': True,
                'scrape_interval_active': 20,
                'scrape_interval_archive': 60,
                'max_articles_per_scrape': 30
            },
            {
                'name': 'Länstidningen Östersund',
                'base_url': 'https://www.ltz.se',
                'scraper_class': 'GenericRSSScraper',
                'is_active': True,
                'scrape_interval_active': 20,
                'scrape_interval_archive': 60,
                'max_articles_per_scrape': 30
            },
            {
                'name': 'Norrbottens-Kuriren',
                'base_url': 'https://www.kuriren.nu',
                'scraper_class': 'GenericRSSScraper',
                'is_active': True,
                'scrape_interval_active': 20,
                'scrape_interval_archive': 60,
                'max_articles_per_scrape': 30
            },
            {
                'name': 'Folkbladet',
                'base_url': 'https://www.folkbladet.se',
                'scraper_class': 'GenericRSSScraper',
                'is_active': True,
                'scrape_interval_active': 20,
                'scrape_interval_archive': 60,
                'max_articles_per_scrape': 30
            },
            {
                'name': 'Barometern',
                'base_url': 'https://www.barometern.se',
                'scraper_class': 'GenericRSSScraper',
                'is_active': True,
                'scrape_interval_active': 20,
                'scrape_interval_archive': 60,
                'max_articles_per_scrape': 30
            },
            {
                'name': 'Smålandsposten',
                'base_url': 'https://www.smp.se',
                'scraper_class': 'GenericRSSScraper',
                'is_active': True,
                'scrape_interval_active': 20,
                'scrape_interval_archive': 60,
                'max_articles_per_scrape': 30
            },
            # Tech/Business
            {
                'name': 'Breakit',
                'base_url': 'https://www.breakit.se',
                'scraper_class': 'GenericRSSScraper',
                'is_active': True,
                'scrape_interval_active': 15,
                'scrape_interval_archive': 60,
                'max_articles_per_scrape': 40
            },
            {
                'name': 'Computer Sweden',
                'base_url': 'https://computersweden.se',
                'scraper_class': 'GenericRSSScraper',
                'is_active': True,
                'scrape_interval_active': 20,
                'scrape_interval_archive': 60,
                'max_articles_per_scrape': 30
            },
            {
                'name': 'IDG.se',
                'base_url': 'https://www.idg.se',
                'scraper_class': 'GenericRSSScraper',
                'is_active': True,
                'scrape_interval_active': 20,
                'scrape_interval_archive': 60,
                'max_articles_per_scrape': 30
            },
        ]

        # For now, mark all as inactive until we create proper scrapers
        # We'll enable them gradually
        for source in sources_to_add:
            source['is_active'] = False

        added = 0
        for source_data in sources_to_add:
            if source_data['name'] not in existing:
                source = NewsSource(**source_data)
                db.add(source)
                print(f"○ Lade till (inaktiv): {source_data['name']}")
                added += 1
            else:
                print(f"✓ Finns redan: {source_data['name']}")

        if added > 0:
            await db.commit()
            print(f"\n○ Totalt {added} nya källor tillagda (som inaktiva)")
            print("  Behöver skapa scrapers innan de aktiveras")
        else:
            print("\n○ Inga nya källor att lägga till")

        # Show all sources
        result = await db.execute(select(NewsSource))
        all_sources = result.scalars().all()
        print(f"\nAlla källor ({len(all_sources)}):")
        active = [s for s in all_sources if s.is_active]
        inactive = [s for s in all_sources if not s.is_active]
        print(f"  Aktiva ({len(active)}):")
        for s in active:
            print(f"    ✓ {s.name}")
        print(f"  Inaktiva ({len(inactive)}):")
        for s in inactive:
            print(f"    ○ {s.name}")


if __name__ == "__main__":
    asyncio.run(add_major_sources())
