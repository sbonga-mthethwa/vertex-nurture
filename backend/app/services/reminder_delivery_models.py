from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ReminderDeliveryStatistics:
    """
    Statistics produced during a reminder delivery run.
    """

    processed: int = 0

    delivered: int = 0

    failed: int = 0

    skipped: int = 0

    def increment_processed(self) -> None:
        self.processed += 1

    def increment_delivered(self) -> None:
        self.delivered += 1

    def increment_failed(self) -> None:
        self.failed += 1

    def increment_skipped(self) -> None:
        self.skipped += 1

    @property
    def success_rate(self) -> float:
        """
        Percentage of processed reminders
        successfully delivered.
        """

        if self.processed == 0:
            return 0.0

        return round(
            (self.delivered / self.processed) * 100,
            2,
        )