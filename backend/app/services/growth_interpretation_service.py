class GrowthInterpretationService:
    """
    Converts WHO Z-scores into clinical interpretations.

    This service contains no mathematical calculations.
    It only interprets already-calculated Z-scores.
    """

    def interpret_weight(
        self,
        z_score: float | None,
    ) -> str | None:
        """
        Returns the weight classification.
        """

        if z_score is None:
            return None

        if z_score < -3:
            return "Severely Underweight"

        if z_score < -2:
            return "Moderately Underweight"

        if z_score <= 2:
            return "Normal"

        if z_score <= 3:
            return "Overweight"

        return "Obese"

    def interpret_height(
        self,
        z_score: float | None,
    ) -> str | None:
        """
        Returns the height classification.
        """

        if z_score is None:
            return None

        if z_score < -3:
            return "Severe Stunting"

        if z_score < -2:
            return "Stunted"

        return "Normal"

    def interpret_bmi(
        self,
        z_score: float | None,
    ) -> str | None:
        """
        Returns the BMI classification.
        """

        if z_score is None:
            return None

        if z_score < -3:
            return "Severe Wasting"

        if z_score < -2:
            return "Wasting"

        if z_score <= 1:
            return "Normal"

        if z_score <= 2:
            return "Risk of Overweight"

        if z_score <= 3:
            return "Overweight"

        return "Obese"

    def interpret_head_circumference(
        self,
        z_score: float | None,
    ) -> str | None:
        """
        Returns the head circumference classification.
        """

        if z_score is None:
            return None

        if z_score < -2:
            return "Microcephaly"

        if z_score > 2:
            return "Macrocephaly"

        return "Normal"