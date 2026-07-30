from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel


class VaccinationStatus(BaseModel):
    vaccine_code: str
    vaccine_name: str
    dose_number: int
    scheduled_age_days: int


class VaccinationAnalysisResponse(BaseModel):
    child_id: UUID

    age_in_days: int

    completion_percentage: float

    completed: list[VaccinationStatus]

    due: list[VaccinationStatus]

    overdue: list[VaccinationStatus]

    upcoming: list[VaccinationStatus]