from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.growth_record import GrowthRecord
from app.repositories.base import BaseRepository


class GrowthRecordRepository(
    BaseRepository[GrowthRecord],
):
    """
    Repository for GrowthRecord entities.
    """

    def __init__(
        self,
        db: AsyncSession,
    ):
        super().__init__(
            db,
            GrowthRecord,
        )

    async def get_by_id(
        self,
        record_id: UUID,
    ) -> GrowthRecord | None:
        """
        Returns a growth record by ID.
        """

        result = await self.db.execute(
            select(GrowthRecord)
            .where(
                GrowthRecord.id == record_id,
            ),
        )

        return result.scalar_one_or_none()

    async def get_by_child(
        self,
        child_id: UUID,
    ) -> list[GrowthRecord]:
        """
        Returns all active growth records for a child.
        """

        result = await self.db.execute(
            select(GrowthRecord)
            .where(
                GrowthRecord.child_id == child_id,
            )
            .where(
                GrowthRecord.is_active.is_(True),
            )
            .order_by(
                GrowthRecord.measurement_date.desc(),
            ),
        )

        return list(
            result.scalars().all(),
        )

    async def get_by_child_and_id(
        self,
        child_id: UUID,
        record_id: UUID,
    ) -> GrowthRecord | None:
        """
        Returns an active growth record belonging to a child.
        """

        result = await self.db.execute(
            select(GrowthRecord)
            .where(
                GrowthRecord.id == record_id,
            )
            .where(
                GrowthRecord.child_id == child_id,
            )
            .where(
                GrowthRecord.is_active.is_(True),
            ),
        )

        return result.scalar_one_or_none()

    async def get_latest_by_child(
        self,
        child_id: UUID,
    ) -> GrowthRecord | None:
        """
        Returns the latest active growth record for a child.
        """

        result = await self.db.execute(
            select(GrowthRecord)
            .where(
                GrowthRecord.child_id == child_id,
            )
            .where(
                GrowthRecord.is_active.is_(True),
            )
            .order_by(
                GrowthRecord.measurement_date.desc(),
            )
            .limit(1),
        )

        return result.scalar_one_or_none()

    async def soft_delete(
        self,
        record: GrowthRecord,
    ) -> GrowthRecord:
        """
        Soft deletes a growth record.
        """

        record.is_active = False

        return await self.update(
            record,
        )