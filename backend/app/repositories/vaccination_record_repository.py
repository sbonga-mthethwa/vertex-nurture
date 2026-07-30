from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.vaccination_record import VaccinationRecord
from app.repositories.base import BaseRepository


class VaccinationRecordRepository(
    BaseRepository[VaccinationRecord],
):
    """
    Repository for VaccinationRecord entities.
    """

    def __init__(
        self,
        db: AsyncSession,
    ):
        super().__init__(
            db,
            VaccinationRecord,
        )

    async def get_by_id(
        self,
        record_id: UUID,
    ) -> VaccinationRecord | None:
        """
        Returns a vaccination record by ID.
        """

        result = await self.db.execute(
            select(VaccinationRecord)
            .where(
                VaccinationRecord.id == record_id,
            ),
        )

        return result.scalar_one_or_none()

    async def get_by_child(
        self,
        child_id: UUID,
    ) -> list[VaccinationRecord]:
        """
        Returns all active vaccination records for a child.
        """

        result = await self.db.execute(
            select(VaccinationRecord)
            .where(
                VaccinationRecord.child_id == child_id,
            )
            .where(
                VaccinationRecord.is_active.is_(True),
            )
            .order_by(
                VaccinationRecord.scheduled_date.desc(),
            ),
        )

        return list(
            result.scalars().all(),
        )

    async def get_by_child_and_id(
        self,
        child_id: UUID,
        record_id: UUID,
    ) -> VaccinationRecord | None:
        """
        Returns an active vaccination record belonging to a child.
        """

        result = await self.db.execute(
            select(VaccinationRecord)
            .where(
                VaccinationRecord.id == record_id,
            )
            .where(
                VaccinationRecord.child_id == child_id,
            )
            .where(
                VaccinationRecord.is_active.is_(True),
            ),
        )

        return result.scalar_one_or_none()

    async def get_upcoming_by_child(
        self,
        child_id: UUID,
    ) -> list[VaccinationRecord]:
        """
        Returns upcoming vaccinations for a child.
        """

        result = await self.db.execute(
            select(VaccinationRecord)
            .where(
                VaccinationRecord.child_id == child_id,
            )
            .where(
                VaccinationRecord.is_active.is_(True),
            )
            .where(
                VaccinationRecord.is_administered.is_(False),
            )
            .order_by(
                VaccinationRecord.scheduled_date.asc(),
            ),
        )

        return list(
            result.scalars().all(),
        )

    async def soft_delete(
        self,
        record: VaccinationRecord,
    ) -> VaccinationRecord:
        """
        Soft deletes a vaccination record.
        """

        record.is_active = False

        return await self.update(
            record,
        )