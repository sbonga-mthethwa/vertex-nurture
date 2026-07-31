from __future__ import annotations

from datetime import date
from enum import Enum
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Boolean,
    Date,
    Enum as SqlEnum,
    ForeignKey,
    Integer,
    String,
    UUID as SQLUUID,
)
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.child import Child
    from app.models.vaccination_record import VaccinationRecord


class ReminderType(str, Enum):
    """
    Reminder interval.
    """

    DAYS_30 = "30_DAYS"
    DAYS_14 = "14_DAYS"
    DAYS_7 = "7_DAYS"
    DAY_1 = "1_DAY"
    DUE_TODAY = "DUE_TODAY"
    OVERDUE = "OVERDUE"


class ReminderStatus(str, Enum):
    """
    Reminder delivery status.
    """

    PENDING = "PENDING"
    SENT = "SENT"
    DISMISSED = "DISMISSED"


class ReminderChannel(str, Enum):
    """
    Delivery channel.
    """

    PUSH = "PUSH"
    EMAIL = "EMAIL"
    SMS = "SMS"


class VaccinationReminder(BaseModel):
    """
    Vaccination reminder.
    """

    __tablename__ = "vaccination_reminders"

    child_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey(
            "children.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    vaccination_record_id: Mapped[UUID | None] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey(
            "vaccination_records.id",
            ondelete="SET NULL",
        ),
        nullable=True,
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

    reminder_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )

    reminder_type: Mapped[ReminderType] = mapped_column(
        SqlEnum(
            ReminderType,
            values_callable=lambda enum: [member.value for member in enum],
        ),
        nullable=False,
    )

    status: Mapped[ReminderStatus] = mapped_column(
        SqlEnum(
            ReminderStatus,
            values_callable=lambda enum: [member.value for member in enum],
        ),
        default=ReminderStatus.PENDING,
        nullable=False,
    )

    channel: Mapped[ReminderChannel] = mapped_column(
        SqlEnum(
            ReminderChannel,
            values_callable=lambda enum: [member.value for member in enum],
        ),
        default=ReminderChannel.PUSH,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    child: Mapped["Child"] = relationship(
        back_populates="vaccination_reminders",
    )

    vaccination_record: Mapped["VaccinationRecord | None"] = relationship(
        back_populates="reminders",
    )