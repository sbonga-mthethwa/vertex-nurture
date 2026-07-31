from datetime import date
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class CreateVaccinationReminderRequest(BaseModel):
    """
    Request model for creating a vaccination reminder.
    """

    child_id: UUID

    vaccination_record_id: UUID | None = None

    vaccine_name: str = Field(
        min_length=1,
        max_length=150,
    )

    dose_number: int = Field(
        ge=1,
    )

    scheduled_date: date

    reminder_date: date

    reminder_type: str = Field(
        min_length=1,
        max_length=30,
    )

    status: str = Field(
        min_length=1,
        max_length=30,
    )

    channel: str = Field(
        min_length=1,
        max_length=20,
    )


class UpdateVaccinationReminderRequest(BaseModel):
    """
    Request model for updating a vaccination reminder.
    """

    reminder_date: date | None = None

    reminder_type: str | None = Field(
        default=None,
        min_length=1,
        max_length=30,
    )

    status: str | None = Field(
        default=None,
        min_length=1,
        max_length=30,
    )

    channel: str | None = Field(
        default=None,
        min_length=1,
        max_length=20,
    )


class VaccinationReminderResponse(BaseModel):
    """
    Response model for vaccination reminders.
    """

    id: UUID

    child_id: UUID

    vaccination_record_id: UUID | None

    vaccine_name: str

    dose_number: int

    scheduled_date: date

    reminder_date: date

    reminder_type: str

    status: str

    channel: str

    is_active: bool

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )