from __future__ import annotations

from datetime import date

from app.models.child import Child
from app.models.vaccination_record import VaccinationRecord
from app.schemas.vaccination_analysis import (
    VaccinationAnalysisResponse,
    VaccinationStatus,
)
from app.services.vaccination_schedule_service import (
    VaccinationScheduleService,
)


class VaccinationAnalysisService:
    """
    Analyses a child's vaccination progress against
    the South African EPI schedule.
    """

    def __init__(
        self,
        schedule_service: VaccinationScheduleService,
    ) -> None:
        self.schedule_service = schedule_service

    ####################################################################
    # Public API
    ####################################################################

    def analyse(
        self,
        *,
        child: Child,
        vaccination_records: list[VaccinationRecord],
        reference_date: date | None = None,
    ) -> VaccinationAnalysisResponse:
        """
        Performs a complete vaccination analysis.
        """

        if reference_date is None:
            reference_date = date.today()

        age_days = self.schedule_service.calculate_age_in_days(
            child.date_of_birth,
            reference_date,
        )

        schedule = self.schedule_service.get_schedule()

        completed = {
            (
                record.vaccine_name,
                record.dose_number,
            )
            for record in vaccination_records
            if record.is_administered
            or record.administered_date is not None
        }

        due: list[VaccinationStatus] = []
        upcoming: list[VaccinationStatus] = []
        overdue: list[VaccinationStatus] = []
        completed_list: list[VaccinationStatus] = []

        for vaccine in schedule:

            key = (
                vaccine["code"],
                vaccine["dose_number"],
            )

            status = VaccinationStatus(
                vaccine_code=vaccine["code"],
                vaccine_name=vaccine["name"],
                dose_number=vaccine["dose_number"],
                scheduled_age_days=vaccine["age_days"],
            )

            if key in completed:
                completed_list.append(status)
                continue

            if vaccine["age_days"] < age_days:
                overdue.append(status)

            elif vaccine["age_days"] == age_days:
                due.append(status)

            else:
                upcoming.append(status)

        completion_percentage = (
            round(
                (
                    len(completed_list)
                    / len(schedule)
                )
                * 100,
                1,
            )
            if schedule
            else 100.0
        )

        return VaccinationAnalysisResponse(
            child_id=child.id,
            age_in_days=age_days,
            completed=completed_list,
            due=due,
            overdue=overdue,
            upcoming=upcoming,
            completion_percentage=completion_percentage,
        )