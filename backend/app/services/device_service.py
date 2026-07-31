from __future__ import annotations

from uuid import UUID

from app.models.device import Device
from app.models.device import DevicePlatform
from app.repositories.device_repository import DeviceRepository


class DeviceService:
    """
    Business logic for registered user devices.
    """

    def __init__(
        self,
        repository: DeviceRepository,
    ) -> None:
        self._repository = repository

    ####################################################################
    # Registration
    ####################################################################

    async def register_device(
        self,
        *,
        user_id: UUID,
        platform: DevicePlatform,
        push_token: str,
        device_name: str | None,
    ) -> Device:
        """
        Registers a user device.

        If the push token already exists, the existing
        record is updated instead of creating a duplicate.
        """

        existing = await self._repository.get_by_push_token(
            push_token,
        )

        if existing is not None:

            existing.user_id = user_id
            existing.platform = platform
            existing.device_name = device_name
            existing.is_active = True

            return await self._repository.update(
                existing,
            )

        device = Device(
            user_id=user_id,
            platform=platform,
            push_token=push_token,
            device_name=device_name,
            is_active=True,
        )

        return await self._repository.create(
            device,
        )

    ####################################################################
    # Retrieval
    ####################################################################

    async def list_user_devices(
        self,
        *,
        user_id: UUID,
    ) -> list[Device]:
        """
        Returns all active devices for a user.
        """

        return await self._repository.list_by_user(
            user_id,
        )

    ####################################################################
    # Deactivation
    ####################################################################

    async def deactivate_device(
        self,
        *,
        push_token: str,
    ) -> Device | None:
        """
        Deactivates a registered device.

        Returns None if the token does not exist.
        """

        device = await self._repository.get_by_push_token(
            push_token,
        )

        if device is None:
            return None

        return await self._repository.deactivate(
            device,
        )