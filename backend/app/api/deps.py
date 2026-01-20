"""API dependencies."""
from typing import AsyncGenerator
from app.database import async_session


async def get_db() -> AsyncGenerator:
    """Get database session."""
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
