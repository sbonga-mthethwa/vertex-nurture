from __future__ import annotations

from decimal import Decimal

from app.models.child import Child
from app.models.growth_record import GrowthRecord
from app.schemas.growth_trend import (
    GrowthAlert,
    GrowthTrendPoint,
    GrowthTrendResponse,
    TrendMetric,
)
from app.services.growth_standard_service import (
    GrowthStandardService,
)


class GrowthTrendService:
    """
    Performs longitudinal growth analysis across
    multiple growth measurements.
    """

    def __init__(
        self,
        growth_standard: GrowthStandardService,
    ) -> None:
        self.growth_standard = growth_standard

    ####################################################################
    # Public API
    ####################################################################

    def analyze_growth_trends(
        self,
        *,
        child: Child,
        growth_records: list[GrowthRecord],
    ) -> GrowthTrendResponse:
        """
        Performs longitudinal WHO growth analysis.
        """

        if not growth_records:
            raise ValueError(
                "No growth records available."
            )

        growth_records = sorted(
            growth_records,
            key=lambda record: record.measurement_date,
        )

        weight = self._analyze_metric(
            growth_records,
            "weight_kg",
        )

        height = self._analyze_metric(
            growth_records,
            "height_cm",
        )

        bmi = self._analyze_metric(
            growth_records,
            "bmi",
        )

        head = self._analyze_metric(
            growth_records,
            "head_circumference_cm",
        )

        alerts = self._generate_alerts(
            child,
            growth_records,
            weight,
            height,
            bmi,
            head,
        )

        summary = self._generate_summary(
            weight,
            height,
            bmi,
            alerts,
        )

        return GrowthTrendResponse(
            summary=summary,
            total_measurements=len(growth_records),
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
                self._build_point(record)
                for record in growth_records
            ],
        )

    ####################################################################
    # Metric Analysis
    ####################################################################

    def _analyze_metric(
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
                previous_record = record
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
            - previous_record.age_in_months,
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

        status = self._determine_status(
            attribute,
            trend,
            velocity,
        )

        return TrendMetric(
            current_value=latest,
            previous_value=previous,
            change=change,
            velocity=velocity,
            trend=trend,
            status=status,
        )

    ####################################################################
    # Status Evaluation
    ####################################################################

    @staticmethod
    def _determine_status(
        attribute: str,
        trend: str,
        velocity: Decimal | None,
    ) -> str:

        if velocity is None:
            return "Unknown"

        #
        # Height should generally increase.
        #

        if (
            attribute == "height_cm"
            and trend == "Declining"
        ):
            return "Needs Review"

        #
        # Weight should generally increase.
        #

        if (
            attribute == "weight_kg"
            and trend == "Declining"
        ):
            return "Needs Review"

        #
        # Head circumference should never decline.
        #

        if (
            attribute == "head_circumference_cm"
            and trend == "Declining"
        ):
            return "Needs Review"

        #
        # Zero growth over time.
        #

        if velocity == Decimal("0.00"):
            return "Monitor"

        return "Normal"

    ####################################################################
    # WHO Growth Evaluation
    ####################################################################

    def _evaluate_latest_measurement(
        self,
        *,
        child: Child,
        record: GrowthRecord,
    ):
        gender = (
            "boys"
            if child.gender.lower() == "male"
            else "girls"
        )

        return {
            "weight": self.growth_standard.evaluate_weight_for_age(
                gender=gender,
                age_in_months=record.age_in_months,
                weight_kg=record.weight_kg,
            ),
            "height": self.growth_standard.evaluate_height_for_age(
                gender=gender,
                age_in_months=record.age_in_months,
                height_cm=record.height_cm,
            ),
            "bmi": self.growth_standard.evaluate_bmi_for_age(
                gender=gender,
                age_in_months=record.age_in_months,
                bmi=record.bmi,
            ),
            "head": self.growth_standard.evaluate_head_circumference(
                gender=gender,
                age_in_months=record.age_in_months,
                head_circumference_cm=record.head_circumference_cm,
            ),
        }

    ####################################################################
    # Alert Generation
    ####################################################################

    def _generate_alerts(
        self,
        child: Child,
        records: list[GrowthRecord],
        weight: TrendMetric | None,
        height: TrendMetric | None,
        bmi: TrendMetric | None,
        head: TrendMetric | None,
    ) -> list[GrowthAlert]:

        alerts: list[GrowthAlert] = []

        latest = records[-1]

        evaluation = self._evaluate_latest_measurement(
            child=child,
            record=latest,
        )

        #
        # WHO Classification alerts
        #

        for result in evaluation.values():

            if result.classification != "Normal":

                alerts.append(
                    GrowthAlert(
                        severity="warning",
                        title=result.classification,
                        description=(
                            f"{result.measurement.replace('_', ' ').title()} "
                            f"is classified as "
                            f"{result.classification} "
                            f"(z-score {result.z_score})."
                        ),
                    )
                )

        #
        # Weight trend
        #

        if (
            weight is not None
            and weight.trend == "Declining"
        ):
            alerts.append(
                GrowthAlert(
                    severity="warning",
                    title="Weight Loss",
                    description=(
                        "Weight has decreased since the previous measurement."
                    ),
                )
            )

        #
        # Height trend
        #

        if (
            height is not None
            and height.trend == "Declining"
        ):
            alerts.append(
                GrowthAlert(
                    severity="critical",
                    title="Height Decrease",
                    description=(
                        "Height should not decrease. Verify measurements."
                    ),
                )
            )

        #
        # Head circumference
        #

        if (
            head is not None
            and head.trend == "Declining"
        ):
            alerts.append(
                GrowthAlert(
                    severity="critical",
                    title="Head Circumference",
                    description=(
                        "Head circumference has decreased."
                    ),
                )
            )

        #
        # BMI
        #

        if (
            bmi is not None
            and bmi.status == "Needs Review"
        ):
            alerts.append(
                GrowthAlert(
                    severity="warning",
                    title="BMI Trend",
                    description=(
                        "BMI trend requires monitoring."
                    ),
                )
            )

        return alerts


    ####################################################################
    # Helper Methods
    ####################################################################

    @staticmethod
    def _determine_trend(
        change: Decimal,
    ) -> str:
        """
        Determines whether a metric is increasing,
        decreasing or stable.
        """

        if change > Decimal("0"):
            return "Increasing"

        if change < Decimal("0"):
            return "Declining"

        return "Stable"

    @staticmethod
    def _build_point(
        record: GrowthRecord,
    ) -> GrowthTrendPoint:
        """
        Converts a GrowthRecord into a trend point.
        """

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
        weight: TrendMetric | None,
        height: TrendMetric | None,
        bmi: TrendMetric | None,
        alerts: list[GrowthAlert],
    ) -> str:
        """
        Generates a human-readable clinical summary.
        """

        #
        # Critical alerts always take precedence.
        #

        if any(
            alert.severity == "critical"
            for alert in alerts
        ):
            return (
                "One or more measurements require immediate clinical review."
            )

        #
        # Warnings
        #

        if any(
            alert.severity == "warning"
            for alert in alerts
        ):
            return (
                "Growth trends show findings that should be monitored closely."
            )

        #
        # Positive growth
        #

        if (
            weight is not None
            and height is not None
            and weight.trend == "Increasing"
            and height.trend == "Increasing"
        ):
            return (
                "Growth is progressing normally with appropriate increases in both weight and height."
            )

        #
        # Stable growth
        #

        if (
            weight is not None
            and height is not None
            and weight.trend == "Stable"
            and height.trend == "Stable"
        ):
            return (
                "Growth measurements are stable since the previous visit."
            )

        #
        # Weight concern
        #

        if (
            weight is not None
            and weight.trend == "Declining"
        ):
            return (
                "Weight has decreased since the previous measurement and should be reviewed."
            )

        #
        # Height concern
        #

        if (
            height is not None
            and height.trend == "Declining"
        ):
            return (
                "Height appears to have decreased. Measurement accuracy should be verified."
            )

        #
        # BMI concern
        #

        if (
            bmi is not None
            and bmi.status != "Normal"
        ):
            return (
                "BMI trend should continue to be monitored."
            )

        #
        # Default
        #

        return (
            "Growth trends are available for review."
        )