from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Boolean,
    Date,
    ForeignKey,
    Numeric,
    String,
    UUID as SQLUUID,
)
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.child import Child


class GrowthRecord(BaseModel):
    """
    Child growth measurements.
    """

    __tablename__ = "growth_records"

    child_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey(
            "children.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    measurement_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    age_in_months: Mapped[int] = mapped_column(
        nullable=False,
    )

    weight_kg: Mapped[Decimal] = mapped_column(
        Numeric(5, 2),
        nullable=False,
    )

    height_cm: Mapped[Decimal] = mapped_column(
        Numeric(5, 2),
        nullable=False,
    )

    head_circumference_cm: Mapped[Decimal | None] = mapped_column(
        Numeric(5, 2),
        nullable=True,
    )

    bmi: Mapped[Decimal | None] = mapped_column(
        Numeric(5, 2),
        nullable=True,
    )

    notes: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    child: Mapped["Child"] = relationship(
        back_populates="growth_records",
    )