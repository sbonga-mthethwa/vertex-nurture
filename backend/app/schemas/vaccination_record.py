from datetime import date
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class CreateVaccinationRecordRequest(BaseModel):
    """
    Request model for creating a vaccination record.
    """

    vaccine_name: str = Field(
        min_length=1,
        max_length=150,
    )

    dose_number: int = Field(
        ge=1,
    )

    scheduled_date: date

    administered_date: date | None = None

    is_administered: bool = False

    facility_name: str | None = Field(
        default=None,
        max_length=150,
    )

    healthcare_provider: str | None = Field(
        default=None,
        max_length=150,
    )

    batch_number: str | None = Field(
        default=None,
        max_length=100,
    )

    notes: str | None = None


class UpdateVaccinationRecordRequest(BaseModel):
    """
    Request model for updating a vaccination record.
    """

    vaccine_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=150,
    )

    dose_number: int | None = Field(
        default=None,
        ge=1,
    )

    scheduled_date: date | None = None

    administered_date: date | None = None

    is_administered: bool | None = None

    facility_name: str | None = Field(
        default=None,
        max_length=150,
    )

    healthcare_provider: str | None = Field(
        default=None,
        max_length=150,
    )

    batch_number: str | None = Field(
        default=None,
        max_length=100,
    )

    notes: str | None = None


class VaccinationRecordResponse(BaseModel):
    """
    Response model for vaccination records.
    """

    id: UUID

    child_id: UUID

    vaccine_name: str

    dose_number: int

    scheduled_date: date

    administered_date: date | None

    is_administered: bool

    facility_name: str | None

    healthcare_provider: str | None

    batch_number: str | None

    notes: str | None

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )