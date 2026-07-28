from datetime import date
from decimal import Decimal

from pydantic import BaseModel
from pydantic import ConfigDict

from app.schemas.growth_evaluation import (
    GrowthEvaluationResult,
)


class GrowthAnalysisResponse(BaseModel):
    """
    Response model for a complete WHO growth analysis.
    """

    measurement_date: date

    age_in_months: int

    bmi: Decimal

    weight: GrowthEvaluationResult

    height: GrowthEvaluationResult

    bmi_evaluation: GrowthEvaluationResult

    head_circumference: GrowthEvaluationResult | None = None

    model_config = ConfigDict(
        from_attributes=True,
    )