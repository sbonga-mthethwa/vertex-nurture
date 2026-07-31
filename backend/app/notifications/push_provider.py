from __future__ import annotations

import logging
from datetime import datetime, UTC
from uuid import uuid4

from app.notifications.base import NotificationProvider
from app.notifications.models import (
    NotificationRequest,
    NotificationResult,
)

logger = logging.getLogger(__name__)


class PushNotificationProvider(NotificationProvider):
    """
    Mock Push Notification Provider.

    This implementation simply logs successful
    deliveries. Later this class will be replaced
    with Firebase Cloud Messaging (FCM),
    OneSignal or Expo Push.
    """

    @property
    def provider_name(self) -> str:
        return "mock_push"

    async def send(
        self,
        request: NotificationRequest,
    ) -> NotificationResult:

        logger.info(
            "Push notification sent | recipient=%s | title=%s",
            request.recipient,
            request.title,
        )

        return NotificationResult(
            success=True,
            provider=self.provider_name,
            message_id=str(uuid4()),
            sent_at=datetime.now(UTC),
            error=None,
        )