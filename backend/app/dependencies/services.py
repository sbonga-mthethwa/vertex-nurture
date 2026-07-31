from typing import Annotated

from fastapi import Depends

from app.dependencies.repositories import (
    get_child_repository,
    get_growth_record_repository,
    get_profile_repository,
    get_refresh_token_repository,
    get_user_repository,
    get_vaccination_record_repository,
    get_vaccination_reminder_repository,
)

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

from app.services import (
    AuthenticationService,
    RefreshTokenService,
    UserService,
)

from app.services.child_service import (
    ChildService,
)

from app.services.growth_analysis_service import (
    GrowthAnalysisService,
)

from app.services.growth_chart_service import (
    GrowthChartService,
)

from app.services.growth_history_service import (
    GrowthHistoryService,
)

from app.services.growth_record_service import (
    GrowthRecordService,
)

from app.services.growth_standard_service import (
    GrowthStandardService,
)

from app.services.growth_trend_service import (
    GrowthTrendService,
)

from app.services.profile_service import (
    ProfileService,
)

from app.services.system_service import (
    SystemService,
)

from app.services.vaccination_schedule_service import (
    VaccinationScheduleService,
)

from app.services.vaccination_analysis_service import (
    VaccinationAnalysisService,
)

from app.services.vaccination_forecast_service import (
    VaccinationForecastService,
)

from app.services.vaccination_record_service import (
    VaccinationRecordService,
)

from app.services.vaccination_reminder_service import (
    VaccinationReminderService,
)


###############################################################################
# Singleton Services
###############################################################################

_growth_standard_service = GrowthStandardService()

_growth_chart_service = GrowthChartService(
    growth_standard_service=_growth_standard_service,
)

_vaccination_schedule_service = VaccinationScheduleService()

_vaccination_forecast_service = VaccinationForecastService(
    schedule_service=_vaccination_schedule_service,
)

_vaccination_analysis_service = VaccinationAnalysisService(
    schedule_service=_vaccination_schedule_service,
)


###############################################################################
# System Services
###############################################################################


def get_system_service() -> SystemService:
    """
    Provides the SystemService.
    """

    return SystemService()


###############################################################################
# Growth Intelligence Services
###############################################################################


def get_growth_standard_service() -> GrowthStandardService:
    """
    Provides the singleton WHO Growth Standards service.
    """

    return _growth_standard_service


def get_growth_analysis_service(
    growth_standard_service: Annotated[
        GrowthStandardService,
        Depends(get_growth_standard_service),
    ],
) -> GrowthAnalysisService:
    """
    Provides the GrowthAnalysisService.
    """

    return GrowthAnalysisService(
        growth_standard_service=growth_standard_service,
    )


def get_growth_trend_service(
    growth_standard: Annotated[
        GrowthStandardService,
        Depends(get_growth_standard_service),
    ],
) -> GrowthTrendService:
    """
    Provides the GrowthTrendService.
    """

    return GrowthTrendService(
        growth_standard=growth_standard,
    )


def get_growth_history_service() -> GrowthHistoryService:
    """
    Provides the GrowthHistoryService.
    """

    return GrowthHistoryService()


def get_growth_chart_service() -> GrowthChartService:
    """
    Provides the singleton GrowthChartService.
    """

    return _growth_chart_service


###############################################################################
# User Services
###############################################################################


async def get_user_service(
    repository: Annotated[
        UserRepository,
        Depends(get_user_repository),
    ],
) -> UserService:
    """
    Provides a UserService.
    """

    return UserService(
        repository,
    )


async def get_refresh_token_service(
    repository: Annotated[
        RefreshTokenRepository,
        Depends(get_refresh_token_repository),
    ],
) -> RefreshTokenService:
    """
    Provides RefreshTokenService.
    """

    return RefreshTokenService(
        repository,
    )


async def get_authentication_service(
    repository: Annotated[
        UserRepository,
        Depends(get_user_repository),
    ],
    refresh_token_service: Annotated[
        RefreshTokenService,
        Depends(get_refresh_token_service),
    ],
) -> AuthenticationService:
    """
    Provides AuthenticationService.
    """

    return AuthenticationService(
        repository,
        refresh_token_service,
    )


async def get_profile_service(
    repository: Annotated[
        ProfileRepository,
        Depends(get_profile_repository),
    ],
) -> ProfileService:
    """
    Provides ProfileService.
    """

    return ProfileService(
        repository,
    )


async def get_child_service(
    repository: Annotated[
        ChildRepository,
        Depends(get_child_repository),
    ],
) -> ChildService:
    """
    Provides ChildService.
    """

    return ChildService(
        repository,
    )


###############################################################################
# Growth Record Service
###############################################################################


async def get_growth_record_service(
    repository: Annotated[
        GrowthRecordRepository,
        Depends(get_growth_record_repository),
    ],
    child_repository: Annotated[
        ChildRepository,
        Depends(get_child_repository),
    ],
    growth_analysis: Annotated[
        GrowthAnalysisService,
        Depends(get_growth_analysis_service),
    ],
    growth_trend: Annotated[
        GrowthTrendService,
        Depends(get_growth_trend_service),
    ],
    growth_history: Annotated[
        GrowthHistoryService,
        Depends(get_growth_history_service),
    ],
    growth_chart: Annotated[
        GrowthChartService,
        Depends(get_growth_chart_service),
    ],
) -> GrowthRecordService:
    """
    Provides GrowthRecordService.
    """

    return GrowthRecordService(
        repository=repository,
        child_repository=child_repository,
        growth_analysis=growth_analysis,
        growth_trend=growth_trend,
        growth_history=growth_history,
        growth_chart=growth_chart,
    )


###############################################################################
# Vaccination Record Service
###############################################################################

def get_vaccination_schedule_service() -> VaccinationScheduleService:
    return _vaccination_schedule_service


def get_vaccination_analysis_service(
) -> VaccinationAnalysisService:
    """
    Provides the singleton VaccinationAnalysisService.
    """

    return _vaccination_analysis_service

def get_vaccination_forecast_service(
) -> VaccinationForecastService:
    return _vaccination_forecast_service

async def get_vaccination_record_service(
    repository: Annotated[
        VaccinationRecordRepository,
        Depends(get_vaccination_record_repository),
    ],
    child_repository: Annotated[
        ChildRepository,
        Depends(get_child_repository),
    ],
    vaccination_analysis: Annotated[
        VaccinationAnalysisService,
        Depends(get_vaccination_analysis_service),
    ],
    vaccination_forecast: Annotated[
        VaccinationForecastService,
        Depends(get_vaccination_forecast_service),
    ],
) -> VaccinationRecordService:
    """
    Provides VaccinationRecordService.
    """

    return VaccinationRecordService(
        repository=repository,
        child_repository=child_repository,
        vaccination_analysis=vaccination_analysis,
        vaccination_forecast=vaccination_forecast,
    )


async def get_vaccination_reminder_service(
    reminder_repository: Annotated[
        VaccinationReminderRepository,
        Depends(get_vaccination_reminder_repository),
    ],
    child_repository: Annotated[
        ChildRepository,
        Depends(get_child_repository),
    ],
    vaccination_record_repository: Annotated[
        VaccinationRecordRepository,
        Depends(get_vaccination_record_repository),
    ],
    vaccination_forecast_service: Annotated[
        VaccinationForecastService,
        Depends(get_vaccination_forecast_service),
    ],
) -> VaccinationReminderService:
    """
    Provides a VaccinationReminderService.
    """

    return VaccinationReminderService(
        repository=reminder_repository,
        child_repository=child_repository,
        vaccination_repository=vaccination_record_repository,
        vaccination_forecast=vaccination_forecast_service,
    )