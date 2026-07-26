from typing import Annotated

from fastapi import Depends

from app.dependencies.repositories import (
    get_refresh_token_repository,
    get_user_repository,
)
from app.repositories import (
    RefreshTokenRepository,
    UserRepository,
)
from app.services import (
    AuthenticationService,
    RefreshTokenService,
    UserService,
)
from app.services.system_service import SystemService


def get_system_service() -> SystemService:
    """
    Provides the SystemService.
    """
    return SystemService()


async def get_user_service(
    repository: Annotated[
        UserRepository,
        Depends(get_user_repository),
    ],
) -> UserService:
    """
    Provides a UserService.
    """
    return UserService(repository)


async def get_refresh_token_service(
    repository: Annotated[
        RefreshTokenRepository,
        Depends(get_refresh_token_repository),
    ],
) -> RefreshTokenService:
    """
    Provides RefreshTokenService.
    """
    return RefreshTokenService(repository)


async def get_authentication_service(
    repository: Annotated[
        UserRepository,
        Depends(get_user_repository),
    ],
    refresh_token_service: Annotated[
        RefreshTokenService,
        Depends(get_refresh_token_service),
    ],
) -> AuthenticationService:
    """
    Provides AuthenticationService.
    """
    return AuthenticationService(
        repository,
        refresh_token_service,
    )