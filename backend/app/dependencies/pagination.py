from fastapi import Depends

from app.shared.pagination import PaginationParams


def get_pagination(
    pagination: PaginationParams = Depends(),
) -> PaginationParams:
    """
    Standard pagination dependency.
    """

    return pagination