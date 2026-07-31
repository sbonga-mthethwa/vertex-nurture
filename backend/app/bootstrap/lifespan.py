from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.bootstrap.scheduler import (
    register_jobs,
    start_scheduler,
    stop_scheduler,
)
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

    # Register scheduled jobs
    register_jobs()

    # Start APScheduler
    start_scheduler()

    yield

    # Stop APScheduler
    stop_scheduler()

    logger.info(
        "application_stopping",
        application=settings.APP_NAME,
    )