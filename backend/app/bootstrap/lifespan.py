from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup and shutdown lifecycle.
    """

    logger.info(
        "application_starting",
        application=settings.APP_NAME,
        version=settings.APP_VERSION,
        environment=settings.APP_ENV,
    )

    # Future startup tasks:
    # - Connect to PostgreSQL
    # - Connect to Redis
    # - Configure monitoring
    # - Load feature flags
    # - Initialize background workers

    yield

    logger.info(
        "application_stopping",
        application=settings.APP_NAME,
    )

    # Future shutdown tasks:
    # - Close PostgreSQL connections
    # - Close Redis connections
    # - Stop background workers
    # - Flush logs