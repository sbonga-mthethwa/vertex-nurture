from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends

from app.api.responses import success_response
from app.core.exceptions import NotFoundError
from app.dependencies import get_system_service
from app.services.system_service import SystemService
from app.shared.pagination import build_pagination
from app.shared.validators import validate_email

router = APIRouter(tags=["System"])


@router.get("/")
async def root(
    service: Annotated[
        SystemService,
        Depends(get_system_service),
    ],
):
    """
    Root endpoint.
    """

    return success_response(
        data=service.get_status(),
        message="Vertex Nurture API is running.",
    )


@router.get("/health")
async def health_check():
    """
    Health check endpoint.
    """

    return success_response(
        data={
            "status": "healthy",
        },
        message="Health check completed.",
    )


@router.get("/test/not-found")
async def test_not_found():
    """
    Test endpoint for global exception handling.
    """

    raise NotFoundError("Child profile not found.")


@router.get("/test/pagination")
async def pagination_test():
    """
    Test endpoint for pagination.
    """

    items = [
        {
            "id": 1,
            "name": "Item 1",
        },
        {
            "id": 2,
            "name": "Item 2",
        },
    ]

    return success_response(
        data=items,
        pagination=build_pagination(
            page=1,
            page_size=20,
            total_items=52,
        ),
    )


@router.get("/test/email")
async def validate_test(email: str):
    """
    Test endpoint for email validation.
    """

    validated = validate_email(email)

    return success_response(
        data={
            "email": validated,
        },
        message="Email validated successfully.",
    )