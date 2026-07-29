from __future__ import annotations

from app.models.child import Child
from app.models.growth_record import GrowthRecord
from app.schemas.growth_history import (
    GrowthHistoryRecord,
    GrowthHistoryResponse,
)


class GrowthHistoryService:
    """
    Produces a chronological growth history for a child.
    """

    ####################################################################
    # Public API
    ####################################################################

    def build_history(
        self,
        *,
        child: Child,
        growth_records: list[GrowthRecord],
    ) -> GrowthHistoryResponse:
        """
        Builds a complete growth history.
        """

        growth_records = sorted(
            growth_records,
            key=lambda r: r.measurement_date,
        )

        history = [
            self._build_record(record)
            for record in growth_records
        ]

        return GrowthHistoryResponse(
            child_id=str(child.id),
            total_measurements=len(history),
            first_measurement=(
                history[0].measurement_date
                if history
                else None
            ),
            latest_measurement=(
                history[-1].measurement_date
                if history
                else None
            ),
            history=history,
        )

    ####################################################################
    # Helpers
    ####################################################################

    @staticmethod
    def _build_record(
        record: GrowthRecord,
    ) -> GrowthHistoryRecord:
        """
        Converts a GrowthRecord into a GrowthHistoryRecord.
        """

        return GrowthHistoryRecord(
            measurement_date=record.measurement_date,
            age_in_months=record.age_in_months,
            weight_kg=record.weight_kg,
            height_cm=record.height_cm,
            bmi=record.bmi,
            head_circumference_cm=(
                record.head_circumference_cm
            ),
            notes=record.notes,
        )