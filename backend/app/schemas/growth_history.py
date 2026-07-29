from __future__ import annotations

from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class GrowthHistoryRecord(BaseModel):
    """
    A single historical growth measurement.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    measurement_date: date
    age_in_months: int

    weight_kg: Decimal
    height_cm: Decimal
    bmi: Decimal | None = None
    head_circumference_cm: Decimal | None = None

    notes: str | None = None


class GrowthHistoryResponse(BaseModel):
    """
    Complete growth history for a child.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    child_id: str

    total_measurements: int

    first_measurement: date | None = None
    latest_measurement: date | None = None

    history: list[GrowthHistoryRecord]