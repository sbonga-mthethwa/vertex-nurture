from datetime import date
from decimal import Decimal, ROUND_HALF_UP

from dateutil.relativedelta import relativedelta

from app.core.exceptions import ValidationError


class GrowthAnalysisService:
    """
    Performs growth calculations and validation for child growth records.
    """

    @staticmethod
    def validate_measurement(
        date_of_birth: date,
        measurement_date: date,
        weight_kg: Decimal,
        height_cm: Decimal,
        head_circumference_cm: Decimal | None = None,
    ) -> None:
        """
        Validates growth measurements.
        """

        today = date.today()

        if measurement_date < date_of_birth:
            raise ValidationError(
                "Measurement date cannot be before the child's date of birth.",
            )

        if measurement_date > today:
            raise ValidationError(
                "Measurement date cannot be in the future.",
            )

        if weight_kg <= Decimal("0"):
            raise ValidationError(
                "Weight must be greater than zero.",
            )

        if weight_kg > Decimal("200"):
            raise ValidationError(
                "Weight exceeds the maximum allowed value.",
            )

        if height_cm <= Decimal("0"):
            raise ValidationError(
                "Height must be greater than zero.",
            )

        if height_cm > Decimal("250"):
            raise ValidationError(
                "Height exceeds the maximum allowed value.",
            )

        if (
            head_circumference_cm is not None
            and head_circumference_cm <= Decimal("0")
        ):
            raise ValidationError(
                "Head circumference must be greater than zero.",
            )

        if (
            head_circumference_cm is not None
            and head_circumference_cm > Decimal("100")
        ):
            raise ValidationError(
                "Head circumference exceeds the maximum allowed value.",
            )

    @staticmethod
    def calculate_age_in_months(
        date_of_birth: date,
        measurement_date: date,
    ) -> int:
        """
        Calculates the child's age in completed months.
        """

        delta = relativedelta(
            measurement_date,
            date_of_birth,
        )

        age_in_months = (
            delta.years * 12
        ) + delta.months

        if age_in_months < 0:
            raise ValidationError(
                "Calculated age cannot be negative.",
            )

        return age_in_months

    @staticmethod
    def calculate_bmi(
        weight_kg: Decimal,
        height_cm: Decimal,
    ) -> Decimal:
        """
        Calculates BMI from weight and height.
        """

        height_m = height_cm / Decimal("100")

        bmi = weight_kg / (
            height_m * height_m
        )

        return bmi.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )