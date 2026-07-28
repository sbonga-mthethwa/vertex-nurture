from datetime import date
from decimal import Decimal
from uuid import UUID

from app.core.exceptions import NotFoundError
from app.models.child import Child
from app.models.growth_record import GrowthRecord
from app.repositories.child_repository import ChildRepository
from app.repositories.growth_record_repository import (
    GrowthRecordRepository,
)
from app.schemas.growth_analysis import (
    GrowthAnalysisResult,
)
from app.schemas.growth_record import (
    CreateGrowthRecordRequest,
    UpdateGrowthRecordRequest,
)
from app.services.growth_analysis_service import (
    GrowthAnalysisService,
)


class GrowthRecordService:
    """
    Business logic for child growth records.
    """

    def __init__(
        self,
        repository: GrowthRecordRepository,
        child_repository: ChildRepository,
        growth_analysis: GrowthAnalysisService,
    ) -> None:
        self.repository = repository
        self.child_repository = child_repository
        self.growth_analysis = growth_analysis

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

    @staticmethod
    def _calculate_age_in_months(
        date_of_birth: date,
        measurement_date: date,
    ) -> int:
        """
        Calculates the completed age in months.
        """

        months = (
            (measurement_date.year - date_of_birth.year) * 12
            + measurement_date.month
            - date_of_birth.month
        )

        if measurement_date.day < date_of_birth.day:
            months -= 1

        return max(months, 0)

    @staticmethod
    def _calculate_bmi(
        weight_kg: Decimal,
        height_cm: Decimal,
    ) -> Decimal:
        """
        Calculates BMI.
        """

        height_m = height_cm / Decimal("100")

        bmi = weight_kg / (height_m * height_m)

        return bmi.quantize(
            Decimal("0.01"),
        )

    ####################################################################
    # CRUD
    ####################################################################

    async def create_growth_record(
        self,
        child_id: UUID,
        parent_id: UUID,
        data: CreateGrowthRecordRequest,
    ) -> GrowthRecord:
        """
        Creates a growth record.
        """

        child = await self._get_child(
            child_id,
            parent_id,
        )

        age_in_months = self._calculate_age_in_months(
            child.date_of_birth,
            data.measurement_date,
        )

        self.growth_analysis.validate_measurement(
            age_in_months=age_in_months,
            weight_kg=data.weight_kg,
            height_cm=data.height_cm,
            head_circumference_cm=data.head_circumference_cm,
        )

        bmi = self._calculate_bmi(
            data.weight_kg,
            data.height_cm,
        )

        growth_record = GrowthRecord(
            child_id=child.id,
            measurement_date=data.measurement_date,
            age_in_months=age_in_months,
            weight_kg=data.weight_kg,
            height_cm=data.height_cm,
            head_circumference_cm=data.head_circumference_cm,
            bmi=bmi,
            notes=data.notes,
        )

        return await self.repository.create(
            growth_record,
        )

    async def list_growth_records(
        self,
        child_id: UUID,
        parent_id: UUID,
    ) -> list[GrowthRecord]:
        """
        Returns all growth records.
        """

        await self._get_child(
            child_id,
            parent_id,
        )

        return await self.repository.get_by_child(
            child_id,
        )

    async def get_growth_record(
        self,
        child_id: UUID,
        record_id: UUID,
        parent_id: UUID,
    ) -> GrowthRecord:
        """
        Returns a single growth record.
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
                "Growth record not found.",
            )

        return record

    async def analyze_growth_record(
        self,
        child_id: UUID,
        record_id: UUID,
        parent_id: UUID,
    ) -> GrowthAnalysisResult:
        """
        Performs WHO growth analysis.
        """

        child = await self._get_child(
            child_id,
            parent_id,
        )

        growth_record = await self.get_growth_record(
            child_id=child_id,
            record_id=record_id,
            parent_id=parent_id,
        )

        return self.growth_analysis.analyze_growth_record(
            child=child,
            growth_record=growth_record,
        )

    async def update_growth_record(
        self,
        child_id: UUID,
        record_id: UUID,
        parent_id: UUID,
        data: UpdateGrowthRecordRequest,
    ) -> GrowthRecord:
        """
        Updates a growth record.
        """

        child = await self._get_child(
            child_id,
            parent_id,
        )

        record = await self.get_growth_record(
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

        age_in_months = self._calculate_age_in_months(
            child.date_of_birth,
            record.measurement_date,
        )

        self.growth_analysis.validate_measurement(
            age_in_months=age_in_months,
            weight_kg=record.weight_kg,
            height_cm=record.height_cm,
            head_circumference_cm=record.head_circumference_cm,
        )

        record.age_in_months = age_in_months

        record.bmi = self._calculate_bmi(
            record.weight_kg,
            record.height_cm,
        )

        return await self.repository.update(
            record,
        )

    async def delete_growth_record(
        self,
        child_id: UUID,
        record_id: UUID,
        parent_id: UUID,
    ) -> None:
        """
        Soft deletes a growth record.
        """

        record = await self.get_growth_record(
            child_id,
            record_id,
            parent_id,
        )

        await self.repository.soft_delete(
            record,
        )