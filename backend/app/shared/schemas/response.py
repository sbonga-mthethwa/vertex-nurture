from typing import Any

from pydantic import BaseModel, Field

from app.shared.pagination import PaginationMetadata


class ApiResponse(BaseModel):
    """
    Standard successful API response.
    """

    success: bool = True

    message: str = Field(
        default="Request completed successfully."
    )

    data: Any | None = None

    pagination: PaginationMetadata | None = None


class ErrorDetail(BaseModel):
    """
    Standard error payload.
    """

    code: str

    message: str


class ErrorResponse(BaseModel):
    """
    Standard error response.
    """

    success: bool = False

    error: ErrorDetail