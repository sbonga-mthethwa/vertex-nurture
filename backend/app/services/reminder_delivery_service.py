from __future__ import annotations

import logging

from app.models.vaccination_reminder import (
    ReminderStatus,
    VaccinationReminder,
)

from app.notifications.factory import NotificationProviderFactory
from app.repositories.vaccination_reminder_repository import (
    VaccinationReminderRepository,
)
from app.services.reminder_delivery_models import (
    ReminderDeliveryStatistics,
)
from app.services.reminder_template_service import (
    ReminderTemplateService,
)

logger = logging.getLogger(__name__)


class ReminderDeliveryService:
    """
    Responsible for delivering vaccination reminders.

    Workflow

    1. Retrieve reminders due today.
    2. Skip inactive reminders.
    3. Skip dismissed reminders.
    4. Build reminder message.
    5. Resolve notification provider.
    6. Send notification.
    7. Mark reminder as SENT.
    8. Continue even if one reminder fails.
    """

    def __init__(
        self,
        repository: VaccinationReminderRepository,
        provider_factory: NotificationProviderFactory,
        template_service: ReminderTemplateService,
    ) -> None:

        self._repository = repository
        self._provider_factory = provider_factory
        self._template_service = template_service

    async def deliver_due_reminders(
        self,
    ) -> ReminderDeliveryStatistics:
        """
        Deliver every reminder that is due today.
        """

        reminders = await self._repository.get_due_reminders()

        statistics = ReminderDeliveryStatistics()

        logger.info(
            "Vaccination reminder delivery started.",
            extra={
                "due_reminders": len(reminders),
            },
        )

        for reminder in reminders:

            statistics.increment_processed()

            if not reminder.is_active:

                statistics.increment_skipped()

                logger.info(
                    "Reminder skipped.",
                    extra={
                        "reminder_id": str(reminder.id),
                        "reason": "inactive",
                    },
                )

                continue

            if reminder.status == ReminderStatus.DISMISSED:

                statistics.increment_skipped()

                logger.info(
                    "Reminder skipped.",
                    extra={
                        "reminder_id": str(reminder.id),
                        "reason": "dismissed",
                    },
                )

                continue

            try:

                await self._deliver_single_reminder(
                    reminder,
                )

                statistics.increment_delivered()

                logger.info(
                    "Reminder delivered.",
                    extra={
                        "reminder_id": str(reminder.id),
                        "child_id": str(reminder.child_id),
                        "channel": reminder.channel.value,
                    },
                )

            except Exception:

                statistics.increment_failed()

                logger.exception(
                    "Reminder delivery failed.",
                    extra={
                        "reminder_id": str(reminder.id),
                        "child_id": str(reminder.child_id),
                        "channel": reminder.channel.value,
                    },
                )

        logger.info(
            "Vaccination reminder delivery completed.",
            extra={
                "processed": statistics.processed,
                "delivered": statistics.delivered,
                "failed": statistics.failed,
                "skipped": statistics.skipped,
                "success_rate": statistics.success_rate,
            },
        )

        return statistics

    async def _deliver_single_reminder(
        self,
        reminder: VaccinationReminder,
    ) -> None:
        """
        Deliver a single reminder.
        """

        message = self._template_service.build_message(
            vaccine_name=reminder.vaccine_name,
            reminder_type=reminder.reminder_type.value,
        )

        provider = self._provider_factory.get_provider(
            reminder.channel,
        )

        await provider.send(
            recipient=str(reminder.child_id),
            title=message.title,
            message=message.body,
        )

        await self._repository.mark_sent(
            reminder,
        )