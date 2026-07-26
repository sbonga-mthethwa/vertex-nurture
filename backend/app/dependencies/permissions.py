from typing import Callable

from fastapi import Depends

from app.core.exceptions import AuthorizationError
from app.dependencies.security import get_current_user
from app.models.user import User, UserRole


def require_roles(
    *roles: UserRole,
) -> Callable:
    """
    Require one or more user roles.
    """

    async def dependency(
        current_user: User = Depends(
            get_current_user,
        ),
    ) -> User:
        if current_user.role not in roles:
            raise AuthorizationError(
                "You don't have permission to perform this action."
            )

        return current_user

    return dependency