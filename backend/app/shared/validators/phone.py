import re


PHONE_REGEX = re.compile(
    r"^\+?[1-9]\d{7,14}$"
)


def validate_phone(phone: str) -> str:
    """
    Validate international phone numbers.
    """

    phone = phone.replace(" ", "")

    if not PHONE_REGEX.match(phone):
        raise ValueError("Invalid phone number.")

    return phone