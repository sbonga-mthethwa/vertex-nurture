from __future__ import annotations

from abc import ABC, abstractmethod

from app.notifications.models import (
    NotificationRequest,
    NotificationResult,
)


class NotificationProvider(ABC):
    """
    Abstract notification provider.

    All notification providers (Push, Email, SMS)
    must implement this interface.
    """

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """
        Returns the provider identifier.
        """
        raise NotImplementedError

    @abstractmethod
    async def send(
        self,
        request: NotificationRequest,
    ) -> NotificationResult:
        """
        Sends a notification.

        Returns a NotificationResult describing
        whether delivery succeeded.
        """
        raise NotImplementedError