from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.child import Child
from app.models.growth_record import GrowthRecord
from app.models.vaccination_record import VaccinationRecord
from app.repositories.base import BaseRepository


class DashboardRepository(BaseRepository[Child]):
    """
    Repository for dashboard queries.
    """

    def __init__(
        self,
        db: AsyncSession,
    ):
        super().__init__(
            db,
            Child,
        )

    async def get_children(
        self,
        parent_id: UUID,
    ) -> list[Child]:
        """
        Returns all active children for the parent.
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

    async def get_latest_growth_records(
        self,
        parent_id: UUID,
    ) -> list[GrowthRecord]:
        """
        Returns growth records for all children belonging
        to the authenticated parent.
        """

        result = await self.db.execute(
            select(GrowthRecord)
            .join(
                Child,
                GrowthRecord.child_id == Child.id,
            )
            .where(
                Child.parent_id == parent_id,
                Child.is_active.is_(True),
            )
            .order_by(
                GrowthRecord.measurement_date.desc(),
            )
        )

        return list(result.scalars().all())

    async def get_upcoming_vaccinations(
        self,
        parent_id: UUID,
    ) -> list[VaccinationRecord]:
        """
        Returns vaccination records belonging
        to the parent's children.
        """

        result = await self.db.execute(
            select(VaccinationRecord)
            .join(
                Child,
                VaccinationRecord.child_id == Child.id,
            )
            .where(
                Child.parent_id == parent_id,
                Child.is_active.is_(True),
            )
            .order_by(
                VaccinationRecord.scheduled_date.asc(),
            )
        )

        return list(result.scalars().all())