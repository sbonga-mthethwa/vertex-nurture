from datetime import date
from uuid import UUID

from app.repositories.dashboard_repository import DashboardRepository

from app.schemas.dashboard import (
    DashboardChild,
    DashboardGrowth,
    DashboardMilestone,
    DashboardResponse,
    DashboardSummary,
    DashboardVaccination,
)


class DashboardService:
    """
    Business logic for the parent dashboard.
    """

    def __init__(
        self,
        repository: DashboardRepository,
    ) -> None:
        self.repository = repository

    async def get_dashboard(
        self,
        parent_id: UUID,
    ) -> DashboardResponse:
        """
        Returns the dashboard for the authenticated parent.
        """

        children = await self.repository.get_children(
            parent_id,
        )

        growth_records = await self.repository.get_latest_growth_records(
            parent_id,
        )

        vaccination_records = await self.repository.get_upcoming_vaccinations(
            parent_id,
        )

        summary = DashboardSummary(
            children_count=len(children),
            upcoming_vaccinations=len(vaccination_records),
            pending_milestones=0,
        )

        return DashboardResponse(
            summary=summary,

            children=[
                DashboardChild(
                    id=child.id,
                    first_name=child.first_name,
                    last_name=child.surname or "",
                    gender=child.gender.value,
                    date_of_birth=child.date_of_birth,
                )
                for child in children
            ],

            growth=[
                DashboardGrowth(
                    child_id=record.child_id,
                    measurement_date=record.measurement_date,
                    weight_kg=record.weight_kg,
                    height_cm=record.height_cm,
                    bmi=record.bmi,
                )
                for record in growth_records
            ],

            vaccinations=[
                DashboardVaccination(
                    child_id=record.child_id,
                    vaccine_name=record.vaccine_name,
                    scheduled_date=record.scheduled_date,
                    administered=record.is_administered,
                )
                for record in vaccination_records
            ],

            milestones=[
                DashboardMilestone(
                    child_id=None,
                    milestone=None,
                    expected_age_months=None,
                    completed=False,
                )
            ],

            recent_activities=[],
        )