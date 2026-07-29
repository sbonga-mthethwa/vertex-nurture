from __future__ import annotations

from decimal import Decimal

from app.models.growth_record import GrowthRecord
from app.schemas.growth_trend import (
    GrowthAlert,
    GrowthTrendPoint,
    GrowthTrendResponse,
    TrendMetric,
)


class GrowthTrendService:
    """
    Analyses longitudinal growth using multiple
    growth records.
    """

    ####################################################################
    # Public API
    ####################################################################

    def analyze_growth_trends(
        self,
        growth_records: list[GrowthRecord],
    ) -> GrowthTrendResponse:
        """
        Analyses a child's longitudinal growth records
        and returns growth trend information.
        """

        if not growth_records:
            raise ValueError(
                "No growth records available."
            )

        growth_records = sorted(
            growth_records,
            key=lambda r: r.measurement_date,
        )

        weight = self._analyse_metric(
            growth_records,
            "weight_kg",
        )

        height = self._analyse_metric(
            growth_records,
            "height_cm",
        )

        bmi = self._analyse_metric(
            growth_records,
            "bmi",
        )

        head = self._analyse_metric(
            growth_records,
            "head_circumference_cm",
        )

        alerts: list[GrowthAlert] = []

        summary = self._generate_summary(
            weight,
            height,
            bmi,
        )

        return GrowthTrendResponse(
            summary=summary,
            total_measurements=len(
                growth_records,
            ),
            first_measurement=growth_records[
                0
            ].measurement_date,
            latest_measurement=growth_records[
                -1
            ].measurement_date,
            weight=weight,
            height=height,
            bmi=bmi,
            head_circumference=head,
            alerts=alerts,
            records=[
                self._build_point(r)
                for r in growth_records
            ],
        )

    ####################################################################
    # Metric Analysis
    ####################################################################

    def _analyse_metric(
        self,
        records: list[GrowthRecord],
        attribute: str,
    ) -> TrendMetric | None:

        latest = getattr(
            records[-1],
            attribute,
        )

        if latest is None:
            return None

        previous = None

        for record in reversed(records[:-1]):
            value = getattr(
                record,
                attribute,
            )

            if value is not None:
                previous = value
                break

        if previous is None:

            return TrendMetric(
                current_value=latest,
                previous_value=None,
                change=None,
                velocity=None,
                trend="Unknown",
                status="Normal",
            )

        change = latest - previous

        months = max(
            records[-1].age_in_months
            - records[-2].age_in_months,
            1,
        )

        velocity = (
            change / Decimal(months)
        ).quantize(
            Decimal("0.01"),
        )

        trend = self._determine_trend(
            change,
        )

        return TrendMetric(
            current_value=latest,
            previous_value=previous,
            change=change,
            velocity=velocity,
            trend=trend,
            status="Normal",
        )

    ####################################################################
    # Helpers
    ####################################################################

    @staticmethod
    def _determine_trend(
        change: Decimal,
    ) -> str:

        if change > Decimal("0"):
            return "Increasing"

        if change < Decimal("0"):
            return "Declining"

        return "Stable"

    @staticmethod
    def _build_point(
        record: GrowthRecord,
    ) -> GrowthTrendPoint:

        return GrowthTrendPoint(
            measurement_date=record.measurement_date,
            age_in_months=record.age_in_months,
            weight_kg=record.weight_kg,
            height_cm=record.height_cm,
            bmi=record.bmi,
            head_circumference_cm=record.head_circumference_cm,
        )

    @staticmethod
    def _generate_summary(
        weight: TrendMetric,
        height: TrendMetric,
        bmi: TrendMetric,
    ) -> str:

        if (
            weight.trend == "Increasing"
            and height.trend == "Increasing"
        ):
            return (
                "Growth is progressing normally."
            )

        if (
            weight.trend == "Declining"
        ):
            return (
                "Weight has decreased since the previous measurement."
            )

        if (
            height.trend == "Declining"
        ):
            return (
                "Height growth appears abnormal."
            )

        return (
            "Growth trend requires monitoring."
        )