import re

EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)


def validate_email(email: str) -> str:
    """
    Validate an email address.
    """

    email = email.strip().lower()

    if not EMAIL_REGEX.match(email):
        raise ValueError("Invalid email address.")

    return email