from uuid import UUID, uuid4

from app.core.exceptions.base import (
    ConflictError,
    NotFoundError,
)
from app.models.user import User
from app.repositories import UserRepository
from app.services.base import BaseService


class UserService(BaseService):
    """
    User business logic.
    """

    def __init__(
        self,
        repository: UserRepository,
    ):
        super().__init__(repository.db)

        self.repository = repository

    async def list_users(self) -> list[User]:
        return await self.repository.get_all()

    async def get_user(
        self,
        user_id: UUID,
    ) -> User:
        user = await self.repository.get_by_id(user_id)

        if user is None:
            raise NotFoundError(
                "User not found."
            )

        return user

    async def create_user(
        self,
        email: str,
        full_name: str,
    ) -> User:

        existing = await self.repository.get_by_email(
            email
        )

        if existing:
            raise ConflictError(
                "A user with this email already exists."
            )

        user = User(
            id=uuid4(),
            email=email,
            full_name=full_name,
            password_hash="",
            is_active=True,
        )

        return await self.repository.create(user)

    async def update_user(
        self,
        user_id: UUID,
        email: str,
        full_name: str,
    ) -> User:
        user = await self.get_user(user_id)

        if user.email != email:
            existing = await self.repository.get_by_email(email)

            if existing:
                raise ConflictError(
                    "A user with this email already exists."
                )

        user.email = email
        user.full_name = full_name

        return await self.repository.update(user)

    async def delete_user(
        self,
        user_id: UUID,
    ) -> None:
        user = await self.get_user(user_id)

        await self.repository.delete(user)