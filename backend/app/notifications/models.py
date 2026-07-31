from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from app.notifications.enums import NotificationChannel


class NotificationRequest(BaseModel):
    """
    Represents a notification to be delivered.
    """

    recipient: str = Field(
        ...,
        description="Destination address, token, phone number or email.",
    )

    title: str = Field(
        ...,
        max_length=200,
    )

    body: str = Field(
        ...,
        max_length=2000,
    )

    channel: NotificationChannel

    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Provider-specific metadata.",
    )


class NotificationResult(BaseModel):
    """
    Result returned by a notification provider.
    """

    success: bool

    provider: str

    message_id: str | None = None

    error: str | None = None

    sent_at: datetime | None = None