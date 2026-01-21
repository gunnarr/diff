import asyncio
from app.database import async_session
from app.services.scraper_service import ScraperService

async def main():
    async with async_session() as db:
        service = ScraperService(db)
        print("Starting manual scrape for source 1 (SVT)...")
        result = await service.scrape_source(1)
        print(f"Result: {result}")

if __name__ == "__main__":
    asyncio.run(main())
