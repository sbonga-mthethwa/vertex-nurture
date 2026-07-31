from __future__ import annotations

import logging

from app.infrastructure.database import (
    AsyncSessionLocal,
)
from app.notifications.factory import (
    NotificationProviderFactory,
)
from app.repositories.vaccination_reminder_repository import (
    VaccinationReminderRepository,
)
from app.services.reminder_delivery_models import (
    ReminderDeliveryStatistics,
)
from app.services.reminder_delivery_service import (
    ReminderDeliveryService,
)
from app.services.reminder_template_service import (
    ReminderTemplateService,
)

logger = logging.getLogger(__name__)


class VaccinationReminderJob:
    """
    Background job responsible for delivering vaccination reminders.

    A fresh database session is created for every execution to avoid
    long-lived SQLAlchemy sessions.
    """

    def __init__(self) -> None:
        self._provider_factory = NotificationProviderFactory()
        self._template_service = ReminderTemplateService()

    async def run(
        self,
    ) -> ReminderDeliveryStatistics:
        """
        Execute one reminder delivery cycle.
        """

        logger.info(
            "Vaccination reminder job started.",
        )

        async with AsyncSessionLocal() as session:

            repository = VaccinationReminderRepository(
                session,
            )

            delivery_service = ReminderDeliveryService(
                repository=repository,
                provider_factory=self._provider_factory,
                template_service=self._template_service,
            )

            statistics = await delivery_service.deliver_due_reminders()

        logger.info(
            "Vaccination reminder job completed.",
            extra={
                "processed": statistics.processed,
                "delivered": statistics.delivered,
                "failed": statistics.failed,
                "skipped": statistics.skipped,
                "success_rate": statistics.success_rate,
            },
        )

        return statistics