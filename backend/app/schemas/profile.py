from pydantic import BaseModel


class ProfileResponse(BaseModel):
    """
    Response schema for a user profile.
    """

    first_name: str | None = None
    surname: str | None = None
    phone_number: str | None = None
    country: str | None = None
    preferred_language: str
    timezone: str

    model_config = {
        "from_attributes": True,
    }


class UpdateProfileRequest(BaseModel):
    """
    Request schema for updating a user profile.
    """

    first_name: str | None = None
    surname: str | None = None
    phone_number: str | None = None
    country: str | None = None
    preferred_language: str | None = None
    timezone: str | None = None