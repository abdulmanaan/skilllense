from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import async_session

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Provide a database session for one request, then close it."""
    async with async_session() as session:
        yield session
