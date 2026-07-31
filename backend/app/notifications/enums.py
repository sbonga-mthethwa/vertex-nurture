from enum import Enum


class NotificationChannel(str, Enum):
    """
    Supported notification delivery channels.
    """

    PUSH = "PUSH"
    EMAIL = "EMAIL"
    SMS = "SMS"