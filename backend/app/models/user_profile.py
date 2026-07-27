from __future__ import annotations

from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class UserProfile(BaseModel):
    """
    Extended profile information for a user.
    """

    __tablename__ = "user_profiles"

    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    first_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    surname: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    phone_number: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    country: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    preferred_language: Mapped[str] = mapped_column(
        String(50),
        default="English",
        nullable=False,
    )

    timezone: Mapped[str] = mapped_column(
        String(100),
        default="Africa/Johannesburg",
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="profile",
    )