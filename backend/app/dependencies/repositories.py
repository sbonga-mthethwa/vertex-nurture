from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.database import get_database
from app.repositories import UserRepository

from app.repositories import RefreshTokenRepository


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