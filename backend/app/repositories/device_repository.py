from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.device import Device
from app.repositories.base import BaseRepository


class DeviceRepository(
    BaseRepository[Device],
):
    """
    Repository for registered devices.
    """

    def __init__(
        self,
        db: AsyncSession,
    ) -> None:
        super().__init__(
            db,
            Device,
        )

    async def get_by_push_token(
        self,
        push_token: str,
    ) -> Device | None:
        """
        Returns a device by push token.
        """

        result = await self.db.execute(
            select(Device).where(
                Device.push_token == push_token,
            )
        )

        return result.scalar_one_or_none()

    async def list_by_user(
        self,
        user_id: UUID,
    ) -> list[Device]:
        """
        Returns every active device belonging to a user.
        """

        result = await self.db.execute(
            select(Device)
            .where(Device.user_id == user_id)
            .where(Device.is_active.is_(True))
        )

        return list(result.scalars().all())

    async def deactivate(
        self,
        device: Device,
    ) -> Device:
        """
        Soft deactivate a device.
        """

        device.is_active = False

        return await self.update(device)