from __future__ import annotations

import json
from datetime import date
from pathlib import Path


class VaccinationScheduleService:
    """
    South African Expanded Programme on Immunisation (EPI) Schedule.

    Responsibilities
    ----------------
    • Load the official vaccination schedule
    • Cache it in memory
    • Determine due vaccines
    • Determine upcoming vaccines
    • Determine overdue vaccines
    """

    def __init__(self) -> None:
        self._schedule_file = (
            Path(__file__).resolve().parent.parent
            / "data"
            / "vaccination"
            / "south_africa"
            / "epi_schedule.json"
        )

        self._schedule: list[dict] = []

        self._load_schedule()

    ####################################################################
    # Loading
    ####################################################################

    def _load_schedule(self) -> None:
        """
        Loads the EPI schedule into memory.
        """

        if not self._schedule_file.exists():
            raise FileNotFoundError(
                f"Vaccination schedule not found: {self._schedule_file}"
            )

        with self._schedule_file.open(
            encoding="utf-8",
        ) as file:
            data = json.load(file)

        self._schedule = sorted(
            data["vaccines"],
            key=lambda vaccine: vaccine["age_days"],
        )

    ####################################################################
    # Public API
    ####################################################################

    def get_schedule(
        self,
    ) -> list[dict]:
        """
        Returns the complete schedule.
        """

        return self._schedule

    def get_vaccine_definition(
        self,
        code: str,
        dose_number: int,
    ) -> dict | None:
        """
        Returns one vaccine definition.
        """

        for vaccine in self._schedule:

            if (
                vaccine["code"] == code
                and vaccine["dose_number"] == dose_number
            ):
                return vaccine

        return None

    ####################################################################
    # Due Vaccines
    ####################################################################

    def get_due_vaccines(
        self,
        age_in_days: int,
    ) -> list[dict]:
        """
        Vaccines due today.
        """

        return [
            vaccine
            for vaccine in self._schedule
            if vaccine["age_days"] == age_in_days
        ]

    ####################################################################
    # Upcoming
    ####################################################################

    def get_upcoming_vaccines(
        self,
        age_in_days: int,
    ) -> list[dict]:
        """
        Vaccines still ahead.
        """

        return [
            vaccine
            for vaccine in self._schedule
            if vaccine["age_days"] > age_in_days
        ]

    ####################################################################
    # Overdue
    ####################################################################

    def get_overdue_vaccines(
        self,
        age_in_days: int,
    ) -> list[dict]:
        """
        Vaccines whose scheduled age has passed.
        """

        return [
            vaccine
            for vaccine in self._schedule
            if vaccine["age_days"] < age_in_days
        ]

    ####################################################################
    # Lookup by Age
    ####################################################################

    def get_schedule_for_age(
        self,
        age_in_days: int,
    ) -> list[dict]:
        """
        Alias for due vaccines.
        """

        return self.get_due_vaccines(
            age_in_days,
        )

    ####################################################################
    # Child Helpers
    ####################################################################

    @staticmethod
    def calculate_age_in_days(
        date_of_birth: date,
        reference_date: date,
    ) -> int:
        """
        Calculates completed age in days.
        """

        return max(
            (reference_date - date_of_birth).days,
            0,
        )