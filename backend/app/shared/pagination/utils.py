import math

from app.shared.pagination.response import PaginationMetadata


def build_pagination(
    *,
    page: int,
    page_size: int,
    total_items: int,
) -> PaginationMetadata:
    """
    Build pagination metadata.
    """

    total_pages = max(
        1,
        math.ceil(total_items / page_size),
    )

    return PaginationMetadata(
        page=page,
        page_size=page_size,
        total_items=total_items,
        total_pages=total_pages,
    )