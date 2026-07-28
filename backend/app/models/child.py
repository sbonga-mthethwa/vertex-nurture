from __future__ import annotations

from datetime import date
from enum import Enum
from typing import TYPE_CHECKING
from uuid import UUID

from decimal import Decimal

from sqlalchemy import (
    Boolean,
    Date,
    Enum as SqlEnum,
    ForeignKey,
    Numeric,
    String,
)
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.growth_record import GrowthRecord


class ChildGender(str, Enum):
    """
    Child gender.
    """

    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"
    UNKNOWN = "Unknown"


class Child(BaseModel):
    """
    Child information.
    """

    __tablename__ = "children"

    parent_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    surname: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    date_of_birth: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    gender: Mapped[ChildGender] = mapped_column(
        SqlEnum(ChildGender),
        nullable=False,
        default=ChildGender.UNKNOWN,
    )

    birth_weight: Mapped[Decimal | None] = mapped_column(
        Numeric(5, 2),
        nullable=True,
    )

    birth_height: Mapped[Decimal | None] = mapped_column(
        Numeric(5, 2),
        nullable=True,
    )

    blood_group: Mapped[str | None] = mapped_column(
        String(5),
        nullable=True,
    )

    allergies: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    medical_conditions: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    parent: Mapped["User"] = relationship(
        back_populates="children",
    )

    growth_records: Mapped[list["GrowthRecord"]] = relationship(
        back_populates="child",
        cascade="all, delete-orphan",
    )