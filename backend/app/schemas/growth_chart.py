from __future__ import annotations

from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field


class GrowthChartPoint(BaseModel):
    """
    A single plotted point.
    """

    measurement_date: date

    age_in_months: int

    value: Decimal

    z_score: Decimal

    percentile: Decimal


class GrowthChartSeries(BaseModel):
    """
    One WHO chart series.
    """

    metric: str

    unit: str

    points: list[GrowthChartPoint]


class GrowthChartsResponse(BaseModel):
    """
    Complete WHO Growth Charts.
    """

    weight_for_age: GrowthChartSeries

    height_for_age: GrowthChartSeries

    bmi_for_age: GrowthChartSeries

    head_circumference_for_age: GrowthChartSeries | None = None