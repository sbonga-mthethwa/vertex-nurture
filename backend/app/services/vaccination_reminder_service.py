from __future__ import annotations

from datetime import date
from datetime import timedelta
from uuid import UUID

from app.core.exceptions import NotFoundError
from app.models.child import Child
from app.models.vaccination_reminder import (
    ReminderChannel,
    ReminderStatus,
    ReminderType,
    VaccinationReminder,
)
from app.repositories.child_repository import ChildRepository
from app.repositories.vaccination_record_repository import (
    VaccinationRecordRepository,
)
from app.repositories.vaccination_reminder_repository import (
    VaccinationReminderRepository,
)
from app.schemas.vaccination_forecast import (
    OverdueVaccinationItem,
    VaccinationForecastItem,
)
from app.services.vaccination_forecast_service import (
    VaccinationForecastService,
)


class VaccinationReminderService:
    """
    Business logic for vaccination reminders.
    """

    REMINDER_OFFSETS: dict[ReminderType, int] = {
        ReminderType.DAYS_30: -30,
        ReminderType.DAYS_14: -14,
        ReminderType.DAYS_7: -7,
        ReminderType.DAY_1: -1,
        ReminderType.DUE_TODAY: 0,
        ReminderType.OVERDUE: 1,
    }

    def __init__(
        self,
        repository: VaccinationReminderRepository,
        child_repository: ChildRepository,
        vaccination_repository: VaccinationRecordRepository,
        vaccination_forecast: VaccinationForecastService,
    ) -> None:
        self.repository = repository
        self.child_repository = child_repository
        self.vaccination_repository = vaccination_repository
        self.vaccination_forecast = vaccination_forecast

    ####################################################################
    # Helpers
    ####################################################################

    async def _get_child(
        self,
        child_id: UUID,
        parent_id: UUID,
    ) -> Child:
        """
        Returns the child after validating ownership.
        """

        child = await self.child_repository.get_by_id(
            child_id,
        )

        if child is None or child.parent_id != parent_id:
            raise NotFoundError(
                "Child not found.",
            )

        return child

    @classmethod
    def _calculate_reminder_date(
        cls,
        scheduled_date: date,
        reminder_type: ReminderType,
    ) -> date:
        """
        Calculates the reminder date for a reminder type.
        """

        return scheduled_date + timedelta(
            days=cls.REMINDER_OFFSETS[reminder_type],
        )

    async def _build_future_reminders(
        self,
        *,
        child: Child,
        vaccine: VaccinationForecastItem,
    ) -> list[VaccinationReminder]:
        """
        Builds reminder entities for a future vaccination.
        Duplicate reminders are skipped.
        """

        reminders: list[VaccinationReminder] = []

        for reminder_type in (
            ReminderType.DAYS_30,
            ReminderType.DAYS_14,
            ReminderType.DAYS_7,
            ReminderType.DAY_1,
            ReminderType.DUE_TODAY,
        ):

            existing = await self.repository.get_existing_reminder(
                child_id=child.id,
                vaccine_name=vaccine.vaccine_name,
                dose_number=vaccine.dose_number,
                reminder_type=reminder_type,
            )

            if existing is not None:
                continue

            reminders.append(
                VaccinationReminder(
                    child_id=child.id,
                    vaccination_record_id=None,
                    vaccine_name=vaccine.vaccine_name,
                    dose_number=vaccine.dose_number,
                    scheduled_date=vaccine.scheduled_date,
                    reminder_date=self._calculate_reminder_date(
                        vaccine.scheduled_date,
                        reminder_type,
                    ),
                    reminder_type=reminder_type,
                    status=ReminderStatus.PENDING,
                    channel=ReminderChannel.PUSH,
                    is_active=True,
                )
            )

        return reminders

    async def _build_overdue_reminder(
        self,
        *,
        child: Child,
        vaccine: OverdueVaccinationItem,
    ) -> VaccinationReminder | None:
        """
        Builds an overdue reminder if one does not already exist.
        """

        existing = await self.repository.get_existing_reminder(
            child_id=child.id,
            vaccine_name=vaccine.vaccine_name,
            dose_number=vaccine.dose_number,
            reminder_type=ReminderType.OVERDUE,
        )

        if existing is not None:
            return None

        return VaccinationReminder(
            child_id=child.id,
            vaccination_record_id=None,
            vaccine_name=vaccine.vaccine_name,
            dose_number=vaccine.dose_number,
            scheduled_date=vaccine.scheduled_date,
            reminder_date=date.today(),
            reminder_type=ReminderType.OVERDUE,
            status=ReminderStatus.PENDING,
            channel=ReminderChannel.PUSH,
            is_active=True,
        )


    ####################################################################
    # Reminder Generation
    ####################################################################

    async def generate_reminders(
        self,
        *,
        child_id: UUID,
        parent_id: UUID,
    ) -> list[VaccinationReminder]:
        """
        Generates reminder records for all outstanding vaccinations.

        This operation is idempotent. Existing reminders are not duplicated.
        """

        child = await self._get_child(
            child_id,
            parent_id,
        )

        vaccination_records = (
            await self.vaccination_repository.get_by_child(
                child.id,
            )
        )

        forecast = self.vaccination_forecast.forecast(
            child=child,
            vaccination_records=vaccination_records,
        )

        created: list[VaccinationReminder] = []

        ################################################################
        # Future vaccinations
        ################################################################

        for vaccine in forecast.future_schedule:

            reminders = await self._build_future_reminders(
                child=child,
                vaccine=vaccine,
            )

            for reminder in reminders:

                created.append(
                    await self.repository.create(
                        reminder,
                    )
                )

        ################################################################
        # Overdue vaccinations
        ################################################################

        for vaccine in forecast.overdue:

            reminder = await self._build_overdue_reminder(
                child=child,
                vaccine=vaccine,
            )

            if reminder is None:
                continue

            created.append(
                await self.repository.create(
                    reminder,
                )
            )

        return created

    async def regenerate_reminders(
        self,
        *,
        child_id: UUID,
        parent_id: UUID,
    ) -> list[VaccinationReminder]:
        """
        Rebuilds reminder records after vaccination history changes.

        Existing reminder records remain intact.
        Missing reminders are generated.
        """

        return await self.generate_reminders(
            child_id=child_id,
            parent_id=parent_id,
        )

    async def sync_child_reminders(
        self,
        *,
        child_id: UUID,
        parent_id: UUID,
    ) -> list[VaccinationReminder]:
        """
        Synchronizes reminders with the child's current forecast.

        Alias around reminder generation used by scheduled jobs.
        """

        return await self.generate_reminders(
            child_id=child_id,
            parent_id=parent_id,
        )

    ####################################################################
    # Retrieval
    ####################################################################

    async def get_reminder(
        self,
        *,
        reminder_id: UUID,
    ) -> VaccinationReminder:
        """
        Returns a reminder.
        """

        reminder = await self.repository.get_by_id(
            reminder_id,
        )

        if reminder is None:
            raise NotFoundError(
                "Vaccination reminder not found.",
            )

        return reminder

    async def list_child_reminders(
        self,
        *,
        child_id: UUID,
        parent_id: UUID,
    ) -> list[VaccinationReminder]:
        """
        Returns all active reminders for a child.
        """

        await self._get_child(
            child_id,
            parent_id,
        )

        return await self.repository.list_by_child(
            child_id,
        )

    async def list_pending_reminders(
        self,
        *,
        child_id: UUID,
        parent_id: UUID,
    ) -> list[VaccinationReminder]:
        """
        Returns pending reminders for a child.
        """

        await self._get_child(
            child_id,
            parent_id,
        )

        return await self.repository.list_pending(
            child_id,
        )


    ####################################################################
    # Due Reminders
    ####################################################################

    async def list_due_reminders(
        self,
        *,
        reminder_date: date | None = None,
    ) -> list[VaccinationReminder]:
        """
        Returns all reminders due for a given day.

        Defaults to today.
        """

        if reminder_date is None:
            reminder_date = date.today()

        return await self.repository.list_due_for_date(
            reminder_date,
        )

    ####################################################################
    # Status Updates
    ####################################################################

    async def mark_sent(
        self,
        *,
        reminder_id: UUID,
    ) -> VaccinationReminder:
        """
        Marks a reminder as sent.
        """

        reminder = await self.get_reminder(
            reminder_id=reminder_id,
        )

        return await self.repository.mark_sent(
            reminder,
        )

    async def dismiss_reminder(
        self,
        *,
        reminder_id: UUID,
    ) -> VaccinationReminder:
        """
        Dismisses a reminder.
        """

        reminder = await self.get_reminder(
            reminder_id=reminder_id,
        )

        return await self.repository.dismiss(
            reminder,
        )

    ####################################################################
    # Delete
    ####################################################################

    async def delete_reminder(
        self,
        *,
        reminder_id: UUID,
    ) -> None:
        """
        Soft deletes a reminder.
        """

        reminder = await self.get_reminder(
            reminder_id=reminder_id,
        )

        await self.repository.soft_delete(
            reminder,
        )