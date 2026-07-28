from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from uuid import UUID

from app.core.exceptions import (
    ConflictError,
    NotFoundError,
    ValidationError,
)
from app.models.child import Child
from app.models.growth_record import GrowthRecord
from app.repositories.child_repository import ChildRepository
from app.repositories.growth_record_repository import (
    GrowthRecordRepository,
)
from app.schemas.growth_record import (
    CreateGrowthRecordRequest,
    UpdateGrowthRecordRequest,
)


class GrowthRecordService:
    """
    Business logic for child growth records.
    """

    def __init__(
        self,
        repository: GrowthRecordRepository,
        child_repository: ChildRepository,
    ):
        self.repository = repository
        self.child_repository = child_repository

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
        birth_date: date,
        measurement_date: date,
    ) -> int:
        """
        Calculates age in completed months.
        """

        months = (
            (measurement_date.year - birth_date.year) * 12
            + measurement_date.month
            - birth_date.month
        )

        if measurement_date.day < birth_date.day:
            months -= 1

        return max(
            months,
            0,
        )

    @staticmethod
    def _calculate_bmi(
        weight_kg: Decimal,
        height_cm: Decimal,
    ) -> Decimal:
        """
        Calculates BMI.
        """

        height_m = height_cm / Decimal("100")

        bmi = weight_kg / (
            height_m * height_m
        )

        return bmi.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

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

        if data.measurement_date < child.date_of_birth:
            raise ValidationError(
                "Measurement date cannot be before the child's date of birth.",
            )

        latest_record = await self.repository.get_latest_by_child(
            child_id,
        )

        if (
            latest_record
            and latest_record.measurement_date == data.measurement_date
        ):
            raise ConflictError(
                "A growth record already exists for this measurement date.",
            )

        growth_record = GrowthRecord(
            child_id=child.id,
            measurement_date=data.measurement_date,
            age_in_months=self._calculate_age_in_months(
                child.date_of_birth,
                data.measurement_date,
            ),
            weight_kg=data.weight_kg,
            height_cm=data.height_cm,
            head_circumference_cm=data.head_circumference_cm,
            bmi=self._calculate_bmi(
                data.weight_kg,
                data.height_cm,
            ),
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
        Returns all growth records for a child.
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
            child_id=child_id,
            record_id=record_id,
            parent_id=parent_id,
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

        if data.measurement_date is not None:
            if data.measurement_date < child.date_of_birth:
                raise ValidationError(
                    "Measurement date cannot be before the child's date of birth.",
                )

            record.age_in_months = self._calculate_age_in_months(
                child.date_of_birth,
                data.measurement_date,
            )

        if (
            data.weight_kg is not None
            or data.height_cm is not None
        ):
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
            child_id=child_id,
            record_id=record_id,
            parent_id=parent_id,
        )

        await self.repository.soft_delete(
            record,
        )