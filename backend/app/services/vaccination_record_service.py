from uuid import UUID

from app.core.exceptions import NotFoundError
from app.models.child import Child
from app.models.vaccination_record import VaccinationRecord

from app.repositories.child_repository import ChildRepository
from app.repositories.vaccination_record_repository import (
    VaccinationRecordRepository,
)

from app.schemas.vaccination_record import (
    CreateVaccinationRecordRequest,
    UpdateVaccinationRecordRequest,
)

from app.services.vaccination_analysis_service import (
    VaccinationAnalysisService,
)

from app.schemas.vaccination_analysis import (
    VaccinationAnalysisResponse,
)

from app.schemas.vaccination_forecast import (
    VaccinationForecastResponse,
)
from app.services.vaccination_forecast_service import (
    VaccinationForecastService,
)


class VaccinationRecordService:
    """
    Business logic for child vaccination records.
    """

    def __init__(
        self,
        repository: VaccinationRecordRepository,
        child_repository: ChildRepository,
        vaccination_analysis: VaccinationAnalysisService,
        vaccination_forecast: VaccinationForecastService,
    ) -> None:
        self.repository = repository
        self.child_repository = child_repository
        self.vaccination_analysis = vaccination_analysis
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

    ####################################################################
    # CRUD
    ####################################################################

    async def create_vaccination_record(
        self,
        child_id: UUID,
        parent_id: UUID,
        data: CreateVaccinationRecordRequest,
    ) -> VaccinationRecord:
        """
        Creates a vaccination record.
        """

        child = await self._get_child(
            child_id,
            parent_id,
        )

        vaccination = VaccinationRecord(
            child_id=child.id,
            vaccine_name=data.vaccine_name,
            dose_number=data.dose_number,
            scheduled_date=data.scheduled_date,
            administered_date=data.administered_date,
            is_administered=data.is_administered,
            facility_name=data.facility_name,
            healthcare_provider=data.healthcare_provider,
            batch_number=data.batch_number,
            notes=data.notes,
        )

        return await self.repository.create(
            vaccination,
        )

    async def list_vaccination_records(
        self,
        child_id: UUID,
        parent_id: UUID,
    ) -> list[VaccinationRecord]:
        """
        Returns all vaccination records.
        """

        await self._get_child(
            child_id,
            parent_id,
        )

        return await self.repository.get_by_child(
            child_id,
        )

    async def get_vaccination_record(
        self,
        child_id: UUID,
        record_id: UUID,
        parent_id: UUID,
    ) -> VaccinationRecord:
        """
        Returns a vaccination record.
        """

        await self._get_child(
            child_id,
            parent_id,
        )

        record = await self.repository.get_by_child_and_id(
            child_id,
            record_id,
        )

        if record is None:
            raise NotFoundError(
                "Vaccination record not found.",
            )

        return record

    async def update_vaccination_record(
        self,
        child_id: UUID,
        record_id: UUID,
        parent_id: UUID,
        data: UpdateVaccinationRecordRequest,
    ) -> VaccinationRecord:
        """
        Updates a vaccination record.
        """

        record = await self.get_vaccination_record(
            child_id,
            record_id,
            parent_id,
        )

        update_data = data.model_dump(
            exclude_unset=True,
        )

        for key, value in update_data.items():
            setattr(
                record,
                key,
                value,
            )

        return await self.repository.update(
            record,
        )

    async def delete_vaccination_record(
        self,
        child_id: UUID,
        record_id: UUID,
        parent_id: UUID,
    ) -> None:
        """
        Soft deletes a vaccination record.
        """

        record = await self.get_vaccination_record(
            child_id,
            record_id,
            parent_id,
        )

        await self.repository.soft_delete(
            record,
        )

    async def get_upcoming_vaccinations(
        self,
        child_id: UUID,
        parent_id: UUID,
    ) -> list[VaccinationRecord]:
        """
        Returns upcoming vaccinations.
        """

        await self._get_child(
            child_id,
            parent_id,
        )

        return await self.repository.get_upcoming_by_child(
            child_id,
        )

    async def get_vaccination_analysis(
        self,
        child_id: UUID,
        parent_id: UUID,
    ) -> VaccinationAnalysisResponse:
        """
        Returns a complete vaccination analysis.
        """

        child = await self._get_child(
            child_id,
            parent_id,
        )

        records = await self.repository.get_by_child(
            child_id,
        )

        return self.vaccination_analysis.analyse(
            child=child,
            vaccination_records=records,
        )

    async def get_vaccination_forecast(
        self,
        *,
        child_id: UUID,
        parent_id: UUID,
    ) -> VaccinationForecastResponse:
        """
        Returns the child's vaccination forecast.
        """

        child = await self._get_child(
            child_id,
            parent_id,
        )

        records = await self.repository.get_by_child(
            child_id,
        )

        return self.vaccination_forecast.forecast(
            child=child,
            vaccination_records=records,
        )