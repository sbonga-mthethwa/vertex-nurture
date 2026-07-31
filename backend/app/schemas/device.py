from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

from app.models.device import DevicePlatform


class DeviceRegisterRequest(BaseModel):
    """
    Request used to register a user device.
    """

    platform: DevicePlatform

    push_token: str = Field(
        min_length=20,
        max_length=500,
    )

    device_name: str | None = Field(
        default=None,
        max_length=150,
    )


class DeviceResponse(BaseModel):
    """
    Device response.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID

    user_id: UUID

    platform: DevicePlatform

    push_token: str

    device_name: str | None

    is_active: bool

    created_at: datetime

    updated_at: datetime