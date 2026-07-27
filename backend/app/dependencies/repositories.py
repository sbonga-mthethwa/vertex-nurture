from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.database import get_database

from app.repositories import (
    RefreshTokenRepository,
    UserRepository,
)

from app.repositories.profile_repository import (
    ProfileRepository,
)

from app.repositories.child_repository import ChildRepository

async def get_user_repository(
    db: Annotated[
        AsyncSession,
        Depends(get_database),
    ],
) -> UserRepository:
    """
    Provides a UserRepository.
    """

    return UserRepository(db)


async def get_refresh_token_repository(
    db: Annotated[
        AsyncSession,
        Depends(get_database),
    ],
) -> RefreshTokenRepository:
    """
    Provides a RefreshTokenRepository.
    """

    return RefreshTokenRepository(db)


async def get_profile_repository(
    db: Annotated[
        AsyncSession,
        Depends(get_database),
    ],
) -> ProfileRepository:
    """
    Provides a ProfileRepository.
    """

    return ProfileRepository(db)


async def get_child_repository(
    session: Annotated[
        AsyncSession,
        Depends(get_database),
    ],
) -> ChildRepository:
    """
    Provides ChildRepository.
    """

    return ChildRepository(session)