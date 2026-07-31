from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from app.api.responses import success_response
from app.dependencies.security import get_current_user
from app.dependencies.services import get_device_service
from app.models.user import User
from app.schemas.device import (
    DeviceRegisterRequest,
    DeviceResponse,
)
from app.services.device_service import DeviceService

router = APIRouter(
    prefix="/devices",
    tags=["Devices"],
)


@router.post(
    "/register",
    response_model=None,
)
async def register_device(
    request: DeviceRegisterRequest,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        DeviceService,
        Depends(get_device_service),
    ],
):
    """
    Register a user device.
    """

    device = await service.register_device(
        user_id=current_user.id,
        platform=request.platform,
        push_token=request.push_token,
        device_name=request.device_name,
    )

    return success_response(
        data=DeviceResponse.model_validate(device),
        message="Device registered successfully.",
    )


@router.get(
    "",
    response_model=None,
)
async def list_devices(
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        DeviceService,
        Depends(get_device_service),
    ],
):
    """
    Returns all active devices for the current user.
    """

    devices = await service.list_user_devices(
        user_id=current_user.id,
    )

    return success_response(
        data=[
            DeviceResponse.model_validate(device)
            for device in devices
        ],
        message="Devices retrieved successfully.",
    )


@router.delete(
    "/{push_token}",
    response_model=None,
)
async def deactivate_device(
    push_token: str,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        DeviceService,
        Depends(get_device_service),
    ],
):
    """
    Deactivate a registered device.
    """

    device = await service.deactivate_device(
        push_token=push_token,
    )

    if device is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found.",
        )

    return success_response(
        data=DeviceResponse.model_validate(device),
        message="Device deactivated successfully.",
    )