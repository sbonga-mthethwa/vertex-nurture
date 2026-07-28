from __future__ import annotations

from datetime import date
from decimal import Decimal

from fastapi.exceptions import ValidationException

from app.models.child import Child
from app.models.growth_record import GrowthRecord
from app.schemas.growth_analysis import (
    GrowthAnalysisResult,
)
from app.services.growth_standard_service import (
    GrowthStandardService,
)


class GrowthAnalysisService:
    """
    Provides complete WHO growth analysis for a child's
    growth record.

    This service orchestrates the WHO Growth Standards Engine
    and combines multiple growth evaluations into a single
    analysis result.
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

    def analyze_growth_record(
        self,
        *,
        child: Child,
        growth_record: GrowthRecord,
    ) -> GrowthAnalysisResult:
        """
        Performs a complete WHO growth analysis for a
        single growth record.
        """

        gender = child.gender.value.lower()

        if gender == "male":
            gender = "boys"
        elif gender == "female":
            gender = "girls"
        else:
            raise ValueError(
                "WHO Growth Standards support only male and female children."
            )

        age_in_months = growth_record.age_in_months

        bmi = (
            growth_record.bmi
            if growth_record.bmi is not None
            else self._calculate_bmi(
                weight_kg=growth_record.weight_kg,
                height_cm=growth_record.height_cm,
            )
        )

        weight = (
            self._growth_standard_service.evaluate_weight_for_age(
                gender=gender,
                age_in_months=age_in_months,
                weight_kg=growth_record.weight_kg,
            )
        )

        height = (
            self._growth_standard_service.evaluate_height_for_age(
                gender=gender,
                age_in_months=age_in_months,
                height_cm=growth_record.height_cm,
            )
        )

        bmi_evaluation = (
            self._growth_standard_service.evaluate_bmi_for_age(
                gender=gender,
                age_in_months=age_in_months,
                bmi=bmi,
            )
        )

        head_circumference = None

        if growth_record.head_circumference_cm is not None:
            head_circumference = (
                self._growth_standard_service.evaluate_head_circumference(
                    gender=gender,
                    age_in_months=age_in_months,
                    head_circumference_cm=(
                        growth_record.head_circumference_cm
                    ),
                )
            )

        return GrowthAnalysisResult(
            measurement_date=growth_record.measurement_date,
            age_in_months=age_in_months,
            bmi=bmi,
            weight=weight,
            height=height,
            bmi_evaluation=bmi_evaluation,
            head_circumference=head_circumference,
        )

    ####################################################################
    # Public Helpers
    ####################################################################

    def calculate_age_in_months(
        self,
        date_of_birth: date,
        measurement_date: date,
    ) -> int:
        """
        Calculates completed age in months.
        """

        months = (
            (measurement_date.year - date_of_birth.year) * 12
            + measurement_date.month
            - date_of_birth.month
        )

        if measurement_date.day < date_of_birth.day:
            months -= 1

        return max(months, 0)

    def calculate_bmi(
        self,
        weight_kg: Decimal,
        height_cm: Decimal,
    ) -> Decimal:
        """
        Public BMI calculator.
        """

        return self._calculate_bmi(
            weight_kg=weight_kg,
            height_cm=height_cm,
        )

    ####################################################################
    # Private Helpers
    ####################################################################

    @staticmethod
    def _calculate_bmi(
        *,
        weight_kg: Decimal,
        height_cm: Decimal,
    ) -> Decimal:
        """
        Calculates BMI from weight and height.
        """

        height_m = height_cm / Decimal("100")

        if height_m <= 0:
            raise ValueError(
                "Height must be greater than zero."
            )

        bmi = weight_kg / (height_m * height_m)

        return bmi.quantize(
            Decimal("0.01"),
        )

    ####################################################################
    # Validation
    ####################################################################

    def validate_measurement(
        self,
        *,
        age_in_months: int,
        weight_kg: Decimal,
        height_cm: Decimal,
        head_circumference_cm: Decimal | None = None,
    ) -> None:
        """
        Validates growth measurements before they are stored.

        Raises:
            ValidationException
        """

        self._validate_age(age_in_months)
        self._validate_weight(weight_kg)
        self._validate_height(height_cm)

        if head_circumference_cm is not None:
            self._validate_head_circumference(
                head_circumference_cm,
            )

    def _validate_age(
        self,
        age_in_months: int,
    ) -> None:
        """
        Validates child age.
        """

        if age_in_months < 0:
            raise ValidationException(
                "Age cannot be negative."
            )

        if age_in_months > 60:
            raise ValidationException(
                "WHO Growth Standards currently support ages 0–60 months."
            )

    def _validate_weight(
        self,
        weight_kg: Decimal,
    ) -> None:
        """
        Validates weight.
        """

        if weight_kg <= Decimal("0"):
            raise ValidationException(
                "Weight must be greater than zero."
            )

        if weight_kg > Decimal("50"):
            raise ValidationException(
                "Weight exceeds the supported range."
            )

    def _validate_height(
        self,
        height_cm: Decimal,
    ) -> None:
        """
        Validates length/height.
        """

        if height_cm <= Decimal("0"):
            raise ValidationException(
                "Height must be greater than zero."
            )

        if height_cm > Decimal("150"):
            raise ValidationException(
                "Height exceeds the supported range."
            )

    def _validate_head_circumference(
        self,
        head_circumference_cm: Decimal,
    ) -> None:
        """
        Validates head circumference.
        """

        if head_circumference_cm <= Decimal("0"):
            raise ValidationException(
                "Head circumference must be greater than zero."
            )

        if head_circumference_cm > Decimal("70"):
            raise ValidationException(
                "Head circumference exceeds the supported range."
            )