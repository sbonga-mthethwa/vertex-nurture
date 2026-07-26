from uuid import UUID


def validate_uuid(value: str) -> str:
    """
    Validate UUID values.
    """

    UUID(value)

    return value