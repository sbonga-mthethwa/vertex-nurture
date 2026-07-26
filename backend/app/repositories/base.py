from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    """
    Base repository for CRUD operations.
    """

    def __init__(
        self,
        db: AsyncSession,
        model: type[ModelType],
    ):
        self.db = db
        self.model = model

    async def get_by_id(self, id):
        statement = select(self.model).where(
            self.model.id == id
        )

        result = await self.db.execute(statement)

        return result.scalar_one_or_none()

    async def get_all(self):
        statement = select(self.model)

        result = await self.db.execute(statement)

        return result.scalars().all()

    async def create(
        self,
        entity: ModelType,
    ):
        self.db.add(entity)

        await self.db.commit()
        await self.db.refresh(entity)

        return entity

    async def update(
        self,
        entity: ModelType,
    ):
        await self.db.commit()
        await self.db.refresh(entity)

        return entity

    async def delete(
        self,
        entity: ModelType,
    ):
        await self.db.delete(entity)
        await self.db.commit()