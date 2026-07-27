from uuid import UUID

from app.models.user_profile import UserProfile
from app.repositories.profile_repository import ProfileRepository


class ProfileService:
    """
    Service responsible for user profile operations.
    """

    def __init__(
        self,
        repository: ProfileRepository,
    ):
        self.repository = repository

    async def get_profile(
        self,
        user_id: UUID,
    ) -> UserProfile:
        """
        Returns a user's profile, creating one if necessary.
        """

        profile = await self.repository.get_by_user_id(
            user_id
        )

        if profile is not None:
            return profile

        profile = UserProfile(
            user_id=user_id,
        )

        return await self.repository.create(
            profile
        )

    async def update_profile(
        self,
        user_id: UUID,
        data,
    ) -> UserProfile:
        """
        Updates a user's profile.
        """

        profile = await self.get_profile(
            user_id
        )

        for field, value in data.model_dump(
            exclude_unset=True,
        ).items():
            setattr(
                profile,
                field,
                value,
            )

        return await self.repository.update(
            profile
        )