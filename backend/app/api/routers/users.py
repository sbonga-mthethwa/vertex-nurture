from typing import Annotated
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends

from app.api.responses import success_response
from app.dependencies import get_user_service
from app.schemas.user import (
    CreateUserRequest,
    UpdateUserRequest,
    UserResponse,
)
from app.services import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("")
async def list_users(
    service: Annotated[
        UserService,
        Depends(get_user_service),
    ],
):
    users = await service.list_users()

    return success_response(
        data=[
            UserResponse.model_validate(user)
            for user in users
        ],
        message="Users retrieved successfully.",
    )


@router.get("/{user_id}")
async def get_user(
    user_id: UUID,
    service: Annotated[
        UserService,
        Depends(get_user_service),
    ],
):
    user = await service.get_user(user_id)

    return success_response(
        data=UserResponse.model_validate(user),
        message="User retrieved successfully.",
    )


@router.post("")
async def create_user(
    request: CreateUserRequest,
    service: Annotated[
        UserService,
        Depends(get_user_service),
    ],
):
    user = await service.create_user(
        email=request.email,
        full_name=request.full_name,
        password=request.password,
    )

    return success_response(
        data=UserResponse.model_validate(user),
        message="User created successfully.",
    )


@router.put("/{user_id}")
async def update_user(
    user_id: UUID,
    request: UpdateUserRequest,
    service: Annotated[
        UserService,
        Depends(get_user_service),
    ],
):
    user = await service.update_user(
        user_id=user_id,
        email=request.email,
        full_name=request.full_name,
    )

    return success_response(
        data=UserResponse.model_validate(user),
        message="User updated successfully.",
    )


@router.delete("/{user_id}")
async def delete_user(
    user_id: UUID,
    service: Annotated[
        UserService,
        Depends(get_user_service),
    ],
):
    await service.delete_user(user_id)

    return success_response(
        message="User deleted successfully.",
    )