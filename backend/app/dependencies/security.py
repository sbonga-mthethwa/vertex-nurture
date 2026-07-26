from typing import Annotated
from uuid import UUID

from fastapi import Depends
from fastapi import Security
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer

from app.core.exceptions import AuthenticationError
from app.dependencies.repositories import get_user_repository
from app.repositories import UserRepository
from app.services.jwt_service import JWTService

bearer_scheme = HTTPBearer()


async def get_current_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials,
        Security(bearer_scheme),
    ],
    repository: Annotated[
        UserRepository,
        Depends(get_user_repository),
    ],
):
    """
    Returns the authenticated user.
    """

    token = credentials.credentials

    jwt_service = JWTService()

    payload = jwt_service.decode_access_token(token)

    user_id = payload.get("sub")

    if user_id is None:
        raise AuthenticationError(
            "Invalid token."
        )

    user = await repository.get_by_id(UUID(user_id))

    if user is None:
        raise AuthenticationError(
            "User no longer exists."
        )

    return user