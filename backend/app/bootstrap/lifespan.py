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

    Startup sequence:
    1. Register scheduled jobs
    2. Start APScheduler
    3. Application ready

    Shutdown sequence:
    1. Stop APScheduler
    2. Shutdown application
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

    try:
        yield
    finally:
        # Stop APScheduler even if an unexpected exception occurs
        stop_scheduler()

        logger.info(
            "application_stopping",
            application=settings.APP_NAME,
        )