from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_profile import UserProfile


class ProfileRepository:
    """
    Repository for user profile operations.
    """

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    async def get_by_user_id(
        self,
        user_id: UUID,
    ) -> UserProfile | None:
        """
        Returns a profile by user id.
        """

        result = await self.db.execute(
            select(UserProfile).where(
                UserProfile.user_id == user_id
            )
        )

        return result.scalar_one_or_none()

    async def create(
        self,
        profile: UserProfile,
    ) -> UserProfile:
        """
        Creates a new profile.
        """

        self.db.add(profile)

        await self.db.commit()
        await self.db.refresh(profile)

        return profile

    async def update(
        self,
        profile: UserProfile,
    ) -> UserProfile:
        """
        Updates an existing profile.
        """

        await self.db.commit()
        await self.db.refresh(profile)

        return profile