from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """
    Repository for User operations.
    """

    def __init__(self, db: AsyncSession):
        super().__init__(db, User)

    async def get_by_email(
        self,
        email: str,
    ) -> User | None:

        statement = select(User).where(
            User.email == email
        )

        result = await self.db.execute(statement)

        return result.scalar_one_or_none()