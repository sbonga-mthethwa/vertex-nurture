from __future__ import annotations

from datetime import date
from datetime import timedelta

from app.models.child import Child
from app.models.vaccination_record import VaccinationRecord
from app.schemas.vaccination_forecast import (
    OverdueVaccinationItem,
    VaccinationForecastItem,
    VaccinationForecastResponse,
)
from app.services.vaccination_schedule_service import (
    VaccinationScheduleService,
)


class VaccinationForecastService:
    """
    Forecasts upcoming vaccinations using the
    South African EPI schedule.
    """

    def __init__(
        self,
        schedule_service: VaccinationScheduleService,
    ) -> None:
        self.schedule_service = schedule_service

    ####################################################################
    # Public API
    ####################################################################

    def forecast(
        self,
        *,
        child: Child,
        vaccination_records: list[VaccinationRecord],
        reference_date: date | None = None,
    ) -> VaccinationForecastResponse:
        """
        Builds the vaccination forecast.
        """

        if reference_date is None:
            reference_date = date.today()

        completed = {
            (
                record.vaccine_name,
                record.dose_number,
            )
            for record in vaccination_records
            if record.administered_date is not None
        }

        future_schedule: list[VaccinationForecastItem] = []
        overdue: list[OverdueVaccinationItem] = []

        schedule = self.schedule_service.get_schedule()

        for vaccine in schedule:

            key = (
                vaccine["code"],
                vaccine["dose_number"],
            )

            if key in completed:
                continue

            scheduled_date = (
                child.date_of_birth
                + timedelta(days=vaccine["age_days"])
            )

            if scheduled_date < reference_date:

                overdue.append(
                    OverdueVaccinationItem(
                        vaccine_code=vaccine["code"],
                        vaccine_name=vaccine["name"],
                        dose_number=vaccine["dose_number"],
                        scheduled_date=scheduled_date,
                        days_overdue=(
                            reference_date
                            - scheduled_date
                        ).days,
                    )
                )

            else:

                future_schedule.append(
                    VaccinationForecastItem(
                        vaccine_code=vaccine["code"],
                        vaccine_name=vaccine["name"],
                        dose_number=vaccine["dose_number"],
                        scheduled_date=scheduled_date,
                        days_until_due=(
                            scheduled_date
                            - reference_date
                        ).days,
                    )
                )

        future_schedule.sort(
            key=lambda x: x.scheduled_date,
        )

        overdue.sort(
            key=lambda x: x.scheduled_date,
        )

        next_vaccination = (
            future_schedule[0]
            if future_schedule
            else None
        )

        return VaccinationForecastResponse(
            child_id=child.id,
            next_vaccination=next_vaccination,
            overdue=overdue,
            future_schedule=future_schedule,
        )