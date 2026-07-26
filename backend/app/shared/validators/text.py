def validate_required_text(
    value: str,
    field_name: str,
) -> str:
    """
    Validate required text fields.
    """

    value = value.strip()

    if not value:
        raise ValueError(
            f"{field_name} is required."
        )

    return value