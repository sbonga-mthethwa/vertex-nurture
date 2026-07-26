from app.shared.pagination import PaginationMetadata
from app.shared.schemas import ApiResponse


def success_response(
    data=None,
    message: str = "Request completed successfully.",
    pagination: PaginationMetadata | None = None,
):
    return ApiResponse(
        success=True,
        message=message,
        data=data,
        pagination=pagination,
    )