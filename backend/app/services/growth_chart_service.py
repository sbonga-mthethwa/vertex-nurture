from __future__ import annotations

from decimal import Decimal

from app.models.child import Child
from app.models.growth_record import GrowthRecord
from app.schemas.growth_chart import (
    GrowthChartPoint,
    GrowthChartSeries,
    GrowthChartsResponse,
)
from app.services.growth_standard_service import (
    GrowthStandardService,
)


class GrowthChartService:
    """
    Builds WHO growth chart datasets from a child's
    historical growth records.
    """

    def __init__(
        self,
        growth_standard_service: GrowthStandardService,
    ) -> None:
        self._growth_standard_service = (
            growth_standard_service
        )

    ####################################################################
    # Public API
    ####################################################################

    def build_growth_charts(
        self,
        *,
        child: Child,
        growth_records: list[GrowthRecord],
    ) -> GrowthChartsResponse:

        if not growth_records:
            raise ValueError(
                "No growth records available."
            )

        gender = child.gender.value.lower()

        if gender == "male":
            gender = "boys"
        elif gender == "female":
            gender = "girls"
        else:
            raise ValueError(
                "WHO Growth Standards support only male and female children."
            )

        growth_records = sorted(
            growth_records,
            key=lambda r: r.measurement_date,
        )

        return GrowthChartsResponse(
            weight_for_age=self._build_weight_chart(
                gender,
                growth_records,
            ),
            height_for_age=self._build_height_chart(
                gender,
                growth_records,
            ),
            bmi_for_age=self._build_bmi_chart(
                gender,
                growth_records,
            ),
            head_circumference_for_age=self._build_head_chart(
                gender,
                growth_records,
            ),
        )

    ####################################################################
    # Weight
    ####################################################################

    def _build_weight_chart(
        self,
        gender: str,
        records: list[GrowthRecord],
    ) -> GrowthChartSeries:

        points: list[GrowthChartPoint] = []

        for record in records:

            result = (
                self._growth_standard_service.evaluate_weight_for_age(
                    gender=gender,
                    age_in_months=record.age_in_months,
                    weight_kg=record.weight_kg,
                )
            )

            points.append(
                GrowthChartPoint(
                    measurement_date=record.measurement_date,
                    age_in_months=record.age_in_months,
                    value=record.weight_kg,
                    z_score=result.z_score,
                    percentile=result.percentile,
                )
            )

        return GrowthChartSeries(
            metric="Weight-for-age",
            unit="kg",
            points=points,
        )

    ####################################################################
    # Height
    ####################################################################

    def _build_height_chart(
        self,
        gender: str,
        records: list[GrowthRecord],
    ) -> GrowthChartSeries:

        points: list[GrowthChartPoint] = []

        for record in records:

            result = (
                self._growth_standard_service.evaluate_height_for_age(
                    gender=gender,
                    age_in_months=record.age_in_months,
                    height_cm=record.height_cm,
                )
            )

            points.append(
                GrowthChartPoint(
                    measurement_date=record.measurement_date,
                    age_in_months=record.age_in_months,
                    value=record.height_cm,
                    z_score=result.z_score,
                    percentile=result.percentile,
                )
            )

        return GrowthChartSeries(
            metric="Height-for-age",
            unit="cm",
            points=points,
        )

    ####################################################################
    # BMI
    ####################################################################

    def _build_bmi_chart(
        self,
        gender: str,
        records: list[GrowthRecord],
    ) -> GrowthChartSeries:

        points: list[GrowthChartPoint] = []

        for record in records:

            result = (
                self._growth_standard_service.evaluate_bmi_for_age(
                    gender=gender,
                    age_in_months=record.age_in_months,
                    bmi=record.bmi,
                )
            )

            points.append(
                GrowthChartPoint(
                    measurement_date=record.measurement_date,
                    age_in_months=record.age_in_months,
                    value=record.bmi,
                    z_score=result.z_score,
                    percentile=result.percentile,
                )
            )

        return GrowthChartSeries(
            metric="BMI-for-age",
            unit="kg/m²",
            points=points,
        )

    ####################################################################
    # Head Circumference
    ####################################################################

    def _build_head_chart(
        self,
        gender: str,
        records: list[GrowthRecord],
    ) -> GrowthChartSeries | None:

        points: list[GrowthChartPoint] = []

        for record in records:

            if record.head_circumference_cm is None:
                continue

            result = (
                self._growth_standard_service.evaluate_head_circumference(
                    gender=gender,
                    age_in_months=record.age_in_months,
                    head_circumference_cm=record.head_circumference_cm,
                )
            )

            points.append(
                GrowthChartPoint(
                    measurement_date=record.measurement_date,
                    age_in_months=record.age_in_months,
                    value=record.head_circumference_cm,
                    z_score=result.z_score,
                    percentile=result.percentile,
                )
            )

        if not points:
            return None

        return GrowthChartSeries(
            metric="Head circumference-for-age",
            unit="cm",
            points=points,
        )