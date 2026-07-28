from decimal import Decimal

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class GrowthEvaluationResult(BaseModel):
    """
    Represents the WHO evaluation of a child's growth measurement.

    This schema is returned by the GrowthStandardService after
    evaluating a measurement against the WHO Child Growth Standards.
    """

    measurement: str = Field(
        description="WHO measurement type.",
        examples=["weight_for_age"],
    )

    gender: str = Field(
        description="Child gender.",
        examples=["boys"],
    )

    age_in_months: int = Field(
        ge=0,
        le=60,
        description="Child age in completed months.",
    )

    measurement_value: Decimal = Field(
        gt=0,
        description="Observed measurement value.",
    )

    unit: str = Field(
        description="Measurement unit.",
        examples=["kg"],
    )

    z_score: Decimal = Field(
        description="WHO LMS z-score.",
    )

    percentile: Decimal = Field(
        ge=0,
        le=100,
        description="WHO percentile.",
    )

    classification: str = Field(
        description="Clinical growth classification.",
        examples=["Normal"],
    )

    l: Decimal = Field(
        description="WHO LMS L parameter.",
    )

    m: Decimal = Field(
        description="WHO LMS M parameter.",
    )

    s: Decimal = Field(
        description="WHO LMS S parameter.",
    )

    model_config = ConfigDict(
        from_attributes=True,
    )