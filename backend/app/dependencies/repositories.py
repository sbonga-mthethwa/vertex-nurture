from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.database import get_database

from app.repositories import (
    RefreshTokenRepository,
    UserRepository,
)
from app.repositories.child_repository import (
    ChildRepository,
)
from app.repositories.growth_record_repository import (
    GrowthRecordRepository,
)
from app.repositories.profile_repository import (
    ProfileRepository,
)
from app.repositories.vaccination_record_repository import (
    VaccinationRecordRepository,
)
from app.repositories.vaccination_reminder_repository import (
    VaccinationReminderRepository,
)
from app.repositories.device_repository import DeviceRepository

from app.repositories.dashboard_repository import (
    DashboardRepository,
)


async def get_user_repository(
    db: Annotated[
        AsyncSession,
        Depends(get_database),
    ],
) -> UserRepository:
    """
    Provides a UserRepository.
    """

    return UserRepository(db)


async def get_refresh_token_repository(
    db: Annotated[
        AsyncSession,
        Depends(get_database),
    ],
) -> RefreshTokenRepository:
    """
    Provides a RefreshTokenRepository.
    """

    return RefreshTokenRepository(db)


async def get_profile_repository(
    db: Annotated[
        AsyncSession,
        Depends(get_database),
    ],
) -> ProfileRepository:
    """
    Provides a ProfileRepository.
    """

    return ProfileRepository(db)


async def get_child_repository(
    db: Annotated[
        AsyncSession,
        Depends(get_database),
    ],
) -> ChildRepository:
    """
    Provides a ChildRepository.
    """

    return ChildRepository(db)


async def get_growth_record_repository(
    db: Annotated[
        AsyncSession,
        Depends(get_database),
    ],
) -> GrowthRecordRepository:
    """
    Provides a GrowthRecordRepository.
    """

    return GrowthRecordRepository(db)

async def get_vaccination_record_repository(
    db: Annotated[
        AsyncSession,
        Depends(get_database),
    ],
) -> VaccinationRecordRepository:
    """
    Provides a VaccinationRecordRepository.
    """

    return VaccinationRecordRepository(db)


async def get_vaccination_reminder_repository(
    db: Annotated[
        AsyncSession,
        Depends(get_database),
    ],
) -> VaccinationReminderRepository:
    """
    Provides a VaccinationReminderRepository.
    """

    return VaccinationReminderRepository(
        db,
    )

def get_device_repository(
    db: Annotated[
        AsyncSession,
        Depends(get_database),
    ],
) -> DeviceRepository:
    """
    Returns the device repository.
    """

    return DeviceRepository(
        db,
    )

async def get_dashboard_repository(
    db: Annotated[
        AsyncSession,
        Depends(get_database),
    ],
) -> DashboardRepository:
    """
    Provides a DashboardRepository.
    """

    return DashboardRepository(
        db,
    )