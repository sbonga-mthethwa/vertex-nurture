from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import EmailStr

from app.models.child import ChildGender


class CreateChildRequest(BaseModel):
    """
    Request for creating a child.
    """

    first_name: str
    surname: str | None = None

    date_of_birth: date

    gender: ChildGender = ChildGender.UNKNOWN

    birth_weight: Decimal | None = None
    birth_height: Decimal | None = None

    blood_group: str | None = None

    allergies: str | None = None
    medical_conditions: str | None = None


class UpdateChildRequest(BaseModel):
    """
    Request for updating a child.
    """

    first_name: str | None = None
    surname: str | None = None

    date_of_birth: date | None = None

    gender: ChildGender | None = None

    birth_weight: Decimal | None = None
    birth_height: Decimal | None = None

    blood_group: str | None = None

    allergies: str | None = None
    medical_conditions: str | None = None

    is_active: bool | None = None


class ChildResponse(BaseModel):
    """
    Child response.
    """

    model_config = ConfigDict(from_attributes=True)

    id: UUID

    first_name: str
    surname: str | None

    date_of_birth: date

    gender: ChildGender

    birth_weight: Decimal | None
    birth_height: Decimal | None

    blood_group: str | None

    allergies: str | None
    medical_conditions: str | None

    is_active: bool

    created_at: datetime
    updated_at: datetime