from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import settings
from app.infrastructure.database.config import database_config

engine = create_async_engine(
    database_config.database_url,
    echo=settings.DATABASE_ECHO,
    future=True,
)