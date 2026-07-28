from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.growth_analysis_response import (
    GrowthAnalysisResponse,
)

class CreateGrowthRecordRequest(BaseModel):
    """
    Request model for creating a growth record.
    """

    measurement_date: date

    weight_kg: Decimal = Field(
        gt=0,
        decimal_places=2,
    )

    height_cm: Decimal = Field(
        gt=0,
        decimal_places=2,
    )

    head_circumference_cm: Decimal | None = Field(
        default=None,
        gt=0,
        decimal_places=2,
    )

    notes: str | None = None


class UpdateGrowthRecordRequest(BaseModel):
    """
    Request model for updating a growth record.
    """

    measurement_date: date | None = None

    weight_kg: Decimal | None = Field(
        default=None,
        gt=0,
        decimal_places=2,
    )

    height_cm: Decimal | None = Field(
        default=None,
        gt=0,
        decimal_places=2,
    )

    head_circumference_cm: Decimal | None = Field(
        default=None,
        gt=0,
        decimal_places=2,
    )

    notes: str | None = None


class GrowthRecordResponse(BaseModel):
    """
    Response model for growth records.
    """

    id: UUID
    child_id: UUID

    measurement_date: date

    age_in_months: int

    weight_kg: Decimal

    height_cm: Decimal

    head_circumference_cm: Decimal | None

    bmi: Decimal | None

    notes: str | None

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )