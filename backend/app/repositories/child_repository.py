from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.child import Child
from app.repositories.base import BaseRepository


class ChildRepository(BaseRepository[Child]):
    """
    Repository for Child entities.
    """

    def __init__(
        self,
        db: AsyncSession,
    ):
        super().__init__(
            db,
            Child,
        )

    async def get_by_id(
        self,
        child_id: UUID,
    ) -> Child | None:
        """
        Returns a child by ID.
        """

        result = await self.db.execute(
            select(Child).where(
                Child.id == child_id,
            )
        )

        return result.scalar_one_or_none()

    async def get_by_parent(
        self,
        parent_id: UUID,
    ) -> list[Child]:
        """
        Returns all children belonging to a parent.
        """

        result = await self.db.execute(
            select(Child)
            .where(
                Child.parent_id == parent_id,
            )
            .order_by(
                Child.date_of_birth.desc(),
            )
        )

        return list(result.scalars().all())

    async def get_active_by_parent(
        self,
        parent_id: UUID,
    ) -> list[Child]:
        """
        Returns all active children belonging to a parent.
        """

        result = await self.db.execute(
            select(Child)
            .where(
                Child.parent_id == parent_id,
                Child.is_active.is_(True),
            )
            .order_by(
                Child.date_of_birth.desc(),
            )
        )

        return list(result.scalars().all())