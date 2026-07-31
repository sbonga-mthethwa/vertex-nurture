"""
Notification-related exceptions.
"""


class NotificationError(Exception):
    """
    Base exception for all notification errors.
    """

    def __init__(self, message: str):
        super().__init__(message)


class ProviderUnavailableError(NotificationError):
    """
    Raised when the selected notification provider is unavailable.
    """

    pass


class DeliveryFailedError(NotificationError):
    """
    Raised when a notification provider attempts delivery but fails.
    """

    pass