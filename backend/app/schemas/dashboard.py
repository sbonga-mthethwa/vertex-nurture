from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class DashboardSummary(BaseModel):
    children_count: int
    upcoming_vaccinations: int
    pending_milestones: int

    model_config = ConfigDict(from_attributes=True)


class DashboardChild(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    gender: str
    date_of_birth: date

    model_config = ConfigDict(from_attributes=True)


class DashboardGrowth(BaseModel):
    child_id: UUID
    measurement_date: date

    weight_kg: Decimal
    height_cm: Decimal
    bmi: Decimal | None = None

    model_config = ConfigDict(from_attributes=True)


class DashboardVaccination(BaseModel):
    child_id: UUID

    vaccine_name: str
    scheduled_date: date
    administered: bool

    model_config = ConfigDict(from_attributes=True)


class DashboardMilestone(BaseModel):
    child_id: UUID | None = None

    milestone: str | None = None
    expected_age_months: int | None = None

    completed: bool = False

    model_config = ConfigDict(from_attributes=True)


class DashboardActivity(BaseModel):
    title: str
    description: str
    occurred_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DashboardResponse(BaseModel):
    summary: DashboardSummary

    children: list[DashboardChild]

    growth: list[DashboardGrowth]

    vaccinations: list[DashboardVaccination]

    milestones: list[DashboardMilestone]

    recent_activities: list[DashboardActivity]

    model_config = ConfigDict(from_attributes=True)