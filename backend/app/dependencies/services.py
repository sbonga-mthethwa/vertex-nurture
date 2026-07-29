from typing import Annotated

from fastapi import Depends

from app.dependencies.repositories import (
    get_child_repository,
    get_growth_record_repository,
    get_profile_repository,
    get_refresh_token_repository,
    get_user_repository,
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

from app.services.growth_history_service import (
    GrowthHistoryService,
)


###############################################################################
# Singleton Services
###############################################################################

_growth_standard_service = GrowthStandardService()


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


def get_growth_trend_service() -> GrowthTrendService:
    """
    Provides the GrowthTrendService.
    """

    return GrowthTrendService()


def get_growth_history_service() -> GrowthHistoryService:
    """
    Provides GrowthHistoryService.
    """

    return GrowthHistoryService()

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
    )