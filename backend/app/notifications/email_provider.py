from __future__ import annotations

import logging
from datetime import UTC, datetime
from uuid import uuid4

from app.notifications.base import NotificationProvider
from app.notifications.models import (
    NotificationRequest,
    NotificationResult,
)

logger = logging.getLogger(__name__)


class EmailNotificationProvider(NotificationProvider):
    """
    Mock Email Notification Provider.

    This implementation logs successful deliveries.

    Future implementation:
    - AWS SES
    - SendGrid
    - SMTP
    """

    @property
    def provider_name(self) -> str:
        return "mock_email"

    async def send(
        self,
        request: NotificationRequest,
    ) -> NotificationResult:

        logger.info(
            "Email notification sent | recipient=%s | title=%s",
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