from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database import AsyncSessionLocal


async def get_database() -> AsyncGenerator[AsyncSession, None]:
    """
    Provides an async database session.
    """

    async with AsyncSessionLocal() as session:
        yield session