from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.responses import success_response
from app.dependencies.security import get_current_user
from app.dependencies.services import get_profile_service
from app.models.user import User
from app.schemas.profile import (
    ProfileResponse,
    UpdateProfileRequest,
)
from app.services.profile_service import ProfileService


router = APIRouter(
    prefix="/profile",
    tags=["Profile"],
)


@router.get("")
async def get_profile(
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        ProfileService,
        Depends(get_profile_service),
    ],
):
    """
    Returns the authenticated user's profile.
    """

    profile = await service.get_profile(
        current_user.id,
    )

    return success_response(
        data=ProfileResponse.model_validate(
            profile,
        ),
        message="Profile retrieved successfully.",
    )


@router.put("")
async def update_profile(
    request: UpdateProfileRequest,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        ProfileService,
        Depends(get_profile_service),
    ],
):
    """
    Updates the authenticated user's profile.
    """

    profile = await service.update_profile(
        current_user.id,
        request,
    )

    return success_response(
        data=ProfileResponse.model_validate(
            profile,
        ),
        message="Profile updated successfully.",
    )