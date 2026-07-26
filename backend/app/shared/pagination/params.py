from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    """
    Standard pagination parameters.
    """

    page: int = Field(
        default=1,
        ge=1,
        description="Page number",
    )

    page_size: int = Field(
        default=20,
        ge=1,
        le=100,
        description="Items per page",
    )

    sort_by: str = Field(
        default="created_at",
        description="Field to sort by",
    )

    sort_order: str = Field(
        default="desc",
        pattern="^(asc|desc)$",
        description="Sort direction",
    )