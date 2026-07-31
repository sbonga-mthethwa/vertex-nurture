from datetime import date
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.vaccination_reminder import (
    ReminderStatus,
    VaccinationReminder,
    ReminderType,
)
from app.repositories.base import BaseRepository


class VaccinationReminderRepository(
    BaseRepository[VaccinationReminder],
):
    """
    Repository for VaccinationReminder entities.
    """

    def __init__(
        self,
        db: AsyncSession,
    ):
        super().__init__(
            db,
            VaccinationReminder,
        )

    async def get_by_id(
        self,
        reminder_id: UUID,
    ) -> VaccinationReminder | None:
        """
        Returns a reminder by ID.
        """

        result = await self.db.execute(
            select(VaccinationReminder)
            .where(
                VaccinationReminder.id == reminder_id,
            ),
        )

        return result.scalar_one_or_none()

    async def list_by_child(
        self,
        child_id: UUID,
    ) -> list[VaccinationReminder]:
        """
        Returns all active reminders for a child.
        """

        result = await self.db.execute(
            select(VaccinationReminder)
            .where(
                VaccinationReminder.child_id == child_id,
            )
            .where(
                VaccinationReminder.is_active.is_(True),
            )
            .order_by(
                VaccinationReminder.reminder_date.asc(),
            ),
        )

        return list(
            result.scalars().all(),
        )

    async def list_pending(
        self,
        child_id: UUID,
    ) -> list[VaccinationReminder]:
        """
        Returns pending reminders.
        """

        result = await self.db.execute(
            select(VaccinationReminder)
            .where(
                VaccinationReminder.child_id == child_id,
            )
            .where(
                VaccinationReminder.status == ReminderStatus.PENDING,
            )
            .where(
                VaccinationReminder.is_active.is_(True),
            )
            .order_by(
                VaccinationReminder.reminder_date.asc(),
            ),
        )

        return list(
            result.scalars().all(),
        )

    async def list_due_for_date(
        self,
        reminder_date: date,
    ) -> list[VaccinationReminder]:
        """
        Returns reminders due on a particular day.
        """

        result = await self.db.execute(
            select(VaccinationReminder)
            .where(
                VaccinationReminder.reminder_date == reminder_date,
            )
            .where(
                VaccinationReminder.status == ReminderStatus.PENDING,
            )
            .where(
                VaccinationReminder.is_active.is_(True),
            ),
        )

        return list(
            result.scalars().all(),
        )

    async def get_existing_reminder(
        self,
        *,
        child_id: UUID,
        vaccine_name: str,
        dose_number: int,
        reminder_type: ReminderType,
    ) -> VaccinationReminder | None:
        """
        Returns an existing active reminder for the same
        vaccine, dose and reminder type.
        """

        result = await self.db.execute(
            select(VaccinationReminder)
            .where(
                VaccinationReminder.child_id == child_id,
            )
            .where(
                VaccinationReminder.vaccine_name == vaccine_name,
            )
            .where(
                VaccinationReminder.dose_number == dose_number,
            )
            .where(
                VaccinationReminder.reminder_type == reminder_type,
            )
            .where(
                VaccinationReminder.is_active.is_(True),
            )
            .limit(1),
        )

        return result.scalar_one_or_none()

    async def mark_sent(
        self,
        reminder: VaccinationReminder,
    ) -> VaccinationReminder:
        """
        Marks a reminder as sent.
        """

        reminder.status = ReminderStatus.SENT

        return await self.update(
            reminder,
        )

    async def dismiss(
        self,
        reminder: VaccinationReminder,
    ) -> VaccinationReminder:
        """
        Dismisses a reminder.
        """

        reminder.status = ReminderStatus.DISMISSED

        return await self.update(
            reminder,
        )

    async def soft_delete(
        self,
        reminder: VaccinationReminder,
    ) -> VaccinationReminder:
        """
        Soft deletes a reminder.
        """

        reminder.is_active = False

        return await self.update(
            reminder,
        )