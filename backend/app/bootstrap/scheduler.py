from __future__ import annotations

import logging
from zoneinfo import ZoneInfo

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.jobs.vaccination_reminder_job import (
    VaccinationReminderJob,
)

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler(
    timezone=ZoneInfo("Africa/Johannesburg"),
)

_reminder_job = VaccinationReminderJob()


def start_scheduler() -> None:
    """
    Starts the application scheduler.
    """

    if scheduler.running:
        return

    scheduler.start()

    logger.info(
        "Background scheduler started.",
    )


def stop_scheduler() -> None:
    """
    Stops the application scheduler.
    """

    if not scheduler.running:
        return

    scheduler.shutdown(wait=False)

    logger.info(
        "Background scheduler stopped.",
    )


def register_jobs() -> None:
    """
    Registers all background jobs.
    """

    scheduler.add_job(
        _reminder_job.run,
        trigger=CronTrigger(
            hour=8,
            minute=0,
        ),
        id="vaccination-reminders",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )

    logger.info(
        "Registered vaccination reminder job.",
    )