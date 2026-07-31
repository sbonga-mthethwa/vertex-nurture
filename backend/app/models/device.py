from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Boolean
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.user import User


class DevicePlatform(str, Enum):
    """
    Supported push notification platforms.
    """

    ANDROID = "ANDROID"
    IOS = "IOS"
    WEB = "WEB"


class Device(BaseModel):
    """
    Registered user device.
    """

    __tablename__ = "devices"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    platform: Mapped[DevicePlatform] = mapped_column(
        SqlEnum(DevicePlatform),
        nullable=False,
    )

    device_name: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    push_token: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        unique=True,
        index=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        back_populates="devices",
    )