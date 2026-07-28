from dataclasses import dataclass


@dataclass(frozen=True)
class WHOGrowthStandard:
    """
    Represents a single WHO LMS reference row.
    """

    age_in_months: int

    l: float

    m: float

    s: float