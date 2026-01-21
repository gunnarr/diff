"""APScheduler setup for periodic scraping."""
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import NewsSource
from app.services.scraper_service import ScraperService
from app.database import async_session
import logging
import httpx

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


async def scrape_source_job(source_id: int):
    """Job to scrape a specific source."""
    async with async_session() as db:
        service = ScraperService(db)
        result = await service.scrape_source(source_id)
        logger.info(f"Scrape job completed for source {source_id}: {result}")


async def run_tests_job():
    """Job to run system tests."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post("http://localhost:8000/api/v1/run-tests", timeout=120.0)
            if response.status_code == 200:
                result = response.json()
                logger.info(f"Daily tests completed: {result['summary']}")
            else:
                logger.error(f"Failed to run tests: HTTP {response.status_code}")
    except Exception as e:
        logger.error(f"Error running scheduled tests: {e}")


async def setup_scheduler():
    """Setup scheduler with jobs for each active source."""
    async with async_session() as db:
        result = await db.execute(
            select(NewsSource).where(NewsSource.is_active == True)
        )
        sources = result.scalars().all()

        for source in sources:
            # Schedule active interval (first 24h)
            scheduler.add_job(
                scrape_source_job,
                trigger=IntervalTrigger(minutes=source.scrape_interval_active),
                args=[source.id],
                id=f'scrape_{source.name}_active',
                replace_existing=True,
                max_instances=1
            )

            logger.info(
                f"Scheduled {source.name} scraping every {source.scrape_interval_active} minutes"
            )

    # Schedule daily system tests at 03:00
    scheduler.add_job(
        run_tests_job,
        trigger=CronTrigger(hour=3, minute=0),
        id='daily_tests',
        replace_existing=True,
        max_instances=1
    )
    logger.info("Scheduled daily system tests at 03:00")

    if not scheduler.running:
        scheduler.start()
        logger.info("Scheduler started")


async def shutdown_scheduler():
    """Shutdown scheduler gracefully."""
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Scheduler shutdown")
