from __future__ import annotations

from app.models.vaccination_reminder import VaccinationReminder
from app.notifications.factory import NotificationProviderFactory
from app.services.reminder_template_service import ReminderTemplateService


class NotificationDispatcher:
    """
    Central notification dispatcher.

    Responsible for:

    • Building notification content.
    • Resolving the correct provider.
    • Sending notifications.

    All application notifications should flow through
    this dispatcher.
    """

    def __init__(
        self,
        provider_factory: NotificationProviderFactory,
        template_service: ReminderTemplateService,
    ) -> None:
        self._provider_factory = provider_factory
        self._template_service = template_service

    async def send_vaccination_reminder(
        self,
        reminder: VaccinationReminder,
    ) -> None:
        """
        Sends a vaccination reminder using the configured
        notification channel.
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