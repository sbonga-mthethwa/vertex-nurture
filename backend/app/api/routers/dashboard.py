from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependencies.security import get_current_user
from app.dependencies.services import get_dashboard_service

from app.models.user import User

from app.schemas.dashboard import DashboardResponse

from app.services.dashboard_service import DashboardService

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "",
    response_model=DashboardResponse,
)
async def get_dashboard(
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    dashboard_service: Annotated[
        DashboardService,
        Depends(get_dashboard_service),
    ],
) -> DashboardResponse:
    """
    Returns the authenticated parent's dashboard.
    """

    return await dashboard_service.get_dashboard(
        current_user.id,
    )