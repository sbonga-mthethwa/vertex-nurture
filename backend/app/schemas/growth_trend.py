from __future__ import annotations

from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field


class TrendMetric(BaseModel):
    """
    Trend analysis for a single measurement.
    """

    current_value: Decimal = Field(
        ...,
        description="Latest recorded value.",
    )

    previous_value: Decimal | None = Field(
        default=None,
        description="Previous recorded value.",
    )

    change: Decimal | None = Field(
        default=None,
        description="Difference between current and previous value.",
    )

    velocity: Decimal | None = Field(
        default=None,
        description="Rate of change per month.",
    )

    trend: str = Field(
        ...,
        description="Increasing, Stable or Declining.",
    )

    status: str = Field(
        ...,
        description="Normal, Warning or Critical.",
    )


class GrowthAlert(BaseModel):
    """
    Clinical alert generated during trend analysis.
    """

    severity: str = Field(
        ...,
        description="info, warning or critical.",
    )

    title: str

    description: str


class GrowthTrendPoint(BaseModel):
    """
    Single point for plotting growth charts.
    """

    measurement_date: date

    age_in_months: int

    weight_kg: Decimal

    height_cm: Decimal

    bmi: Decimal

    head_circumference_cm: Decimal | None = None


class GrowthTrendResponse(BaseModel):
    """
    Complete longitudinal growth analysis.
    """

    summary: str

    total_measurements: int

    first_measurement: date

    latest_measurement: date

    weight: TrendMetric

    height: TrendMetric

    bmi: TrendMetric

    head_circumference: TrendMetric | None = None

    alerts: list[GrowthAlert] = Field(
        default_factory=list,
    )

    records: list[GrowthTrendPoint] = Field(
        default_factory=list,
    )