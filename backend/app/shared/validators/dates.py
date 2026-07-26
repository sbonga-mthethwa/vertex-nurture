from datetime import date


def validate_birth_date(
    birth_date: date,
) -> date:
    """
    Validate child birth date.
    """

    if birth_date > date.today():
        raise ValueError(
            "Birth date cannot be in the future."
        )

    return birth_date