from __future__ import annotations

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