from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ReminderMessage:
    """
    Fully rendered reminder notification.
    """

    title: str
    body: str


class ReminderTemplateService:
    """
    Responsible for rendering reminder
    notification templates.
    """

    def build_message(
        self,
        *,
        vaccine_name: str,
        reminder_type: str,
    ) -> ReminderMessage:
        """
        Creates a notification title and body
        based on the reminder type.
        """

        reminder_type = reminder_type.upper()

        title = "Vaccination Reminder"

        if reminder_type == "30_DAYS":
            body = (
                f"Your child is due for the "
                f"{vaccine_name} vaccine in 30 days."
            )

        elif reminder_type == "14_DAYS":
            body = (
                f"Your child is due for the "
                f"{vaccine_name} vaccine in 14 days."
            )

        elif reminder_type == "7_DAYS":
            body = (
                f"Your child is due for the "
                f"{vaccine_name} vaccine in one week."
            )

        elif reminder_type == "1_DAY":
            body = (
                f"Your child is due for the "
                f"{vaccine_name} vaccine tomorrow."
            )

        elif reminder_type == "DUE_TODAY":
            title = "Vaccination Due Today"

            body = (
                f"Your child is due for the "
                f"{vaccine_name} vaccine today."
            )

        elif reminder_type == "OVERDUE":
            title = "Vaccination Overdue"

            body = (
                f"Your child is overdue for the "
                f"{vaccine_name} vaccine."
            )

        else:
            body = (
                f"Your child has an upcoming "
                f"{vaccine_name} vaccination."
            )

        return ReminderMessage(
            title=title,
            body=body,
        )