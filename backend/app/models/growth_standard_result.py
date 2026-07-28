from dataclasses import dataclass


@dataclass(frozen=True)
class GrowthStandardResult:
    """
    Result returned by WHO growth evaluation.
    """

    z_score: float

    percentile: float

    status: str