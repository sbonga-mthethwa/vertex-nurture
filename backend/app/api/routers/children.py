from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends

from app.api.responses import success_response
from app.dependencies.security import get_current_user
from app.dependencies.services import get_child_service
from app.models.user import User
from app.schemas.child import (
    ChildResponse,
    CreateChildRequest,
    UpdateChildRequest,
)
from app.services.child_service import ChildService

router = APIRouter(
    prefix="/children",
    tags=["Children"],
)


@router.get("")
async def list_children(
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        ChildService,
        Depends(get_child_service),
    ],
):
    """
    Returns all children belonging to the authenticated parent.
    """

    children = await service.list_children(
        current_user.id,
    )

    return success_response(
        data=[
            ChildResponse.model_validate(child)
            for child in children
        ],
        message="Children retrieved successfully.",
    )


@router.get("/{child_id}")
async def get_child(
    child_id: UUID,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        ChildService,
        Depends(get_child_service),
    ],
):
    """
    Returns a single child.
    """

    child = await service.get_child(
        child_id,
        current_user.id,
    )

    return success_response(
        data=ChildResponse.model_validate(
            child,
        ),
        message="Child retrieved successfully.",
    )


@router.post("")
async def create_child(
    request: CreateChildRequest,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        ChildService,
        Depends(get_child_service),
    ],
):
    """
    Creates a child.
    """

    child = await service.create_child(
        parent_id=current_user.id,
        first_name=request.first_name,
        surname=request.surname,
        date_of_birth=request.date_of_birth,
        gender=request.gender,
        birth_weight=request.birth_weight,
        birth_height=request.birth_height,
        blood_group=request.blood_group,
        allergies=request.allergies,
        medical_conditions=request.medical_conditions,
    )

    return success_response(
        data=ChildResponse.model_validate(
            child,
        ),
        message="Child created successfully.",
    )


@router.put("/{child_id}")
async def update_child(
    child_id: UUID,
    request: UpdateChildRequest,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        ChildService,
        Depends(get_child_service),
    ],
):
    """
    Updates a child.
    """

    child = await service.update_child(
        child_id,
        current_user.id,
        request,
    )

    return success_response(
        data=ChildResponse.model_validate(
            child,
        ),
        message="Child updated successfully.",
    )


@router.delete("/{child_id}")
async def delete_child(
    child_id: UUID,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        ChildService,
        Depends(get_child_service),
    ],
):
    """
    Soft deletes a child.
    """

    await service.delete_child(
        child_id,
        current_user.id,
    )

    return success_response(
        message="Child deleted successfully.",
    )