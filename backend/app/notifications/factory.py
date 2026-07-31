from __future__ import annotations

from app.notifications.base import NotificationProvider
from app.notifications.email_provider import (
    EmailNotificationProvider,
)
from app.notifications.enums import NotificationChannel
from app.notifications.exceptions import (
    ProviderUnavailableError,
)
from app.notifications.push_provider import (
    PushNotificationProvider,
)
from app.notifications.sms_provider import (
    SmsNotificationProvider,
)


class NotificationProviderFactory:
    """
    Factory responsible for resolving the correct
    notification provider for a delivery channel.
    """

    def __init__(self) -> None:

        self._providers: dict[
            NotificationChannel,
            NotificationProvider,
        ] = {
            NotificationChannel.PUSH: PushNotificationProvider(),
            NotificationChannel.EMAIL: EmailNotificationProvider(),
            NotificationChannel.SMS: SmsNotificationProvider(),
        }

    def get_provider(
        self,
        channel: NotificationChannel,
    ) -> NotificationProvider:
        """
        Returns the provider responsible for the
        requested notification channel.
        """

        provider = self._providers.get(channel)

        if provider is None:
            raise ProviderUnavailableError(
                f"No notification provider registered for '{channel.value}'."
            )

        return provider