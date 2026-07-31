from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Boolean,
    Date,
    ForeignKey,
    Integer,
    String,
    UUID as SQLUUID,
)
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.models.base import BaseModel
from app.models.vaccination_reminder import VaccinationReminder

if TYPE_CHECKING:
    from app.models.child import Child


class VaccinationRecord(BaseModel):
    """
    Child vaccination record.
    """

    __tablename__ = "vaccination_records"

    child_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey(
            "children.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    vaccine_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    dose_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    scheduled_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    administered_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    is_administered: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    facility_name: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    healthcare_provider: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    batch_number: Mapped[str | None] = mapped_column(
        String(100),
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
        back_populates="vaccination_records",
    )

    reminders: Mapped[list["VaccinationReminder"]] = relationship(
        back_populates="vaccination_record",
    )