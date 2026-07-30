from datetime import date
from uuid import UUID

from pydantic import BaseModel


class VaccinationForecastItem(BaseModel):
    vaccine_code: str
    vaccine_name: str
    dose_number: int
    scheduled_date: date
    days_until_due: int


class OverdueVaccinationItem(BaseModel):
    vaccine_code: str
    vaccine_name: str
    dose_number: int
    scheduled_date: date
    days_overdue: int


class VaccinationForecastResponse(BaseModel):
    child_id: UUID
    next_vaccination: VaccinationForecastItem | None
    overdue: list[OverdueVaccinationItem]
    future_schedule: list[VaccinationForecastItem]