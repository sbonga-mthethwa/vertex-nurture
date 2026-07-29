from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends

from app.api.responses import success_response
from app.dependencies.security import get_current_user
from app.dependencies.services import get_growth_record_service
from app.models.user import User
from app.schemas.growth_analysis import (
    GrowthAnalysisResult,
)
from app.schemas.growth_history import (
    GrowthHistoryResponse,
)
from app.schemas.growth_record import (
    CreateGrowthRecordRequest,
    GrowthRecordResponse,
    UpdateGrowthRecordRequest,
)
from app.schemas.growth_trend import (
    GrowthTrendResponse,
)
from app.services.growth_record_service import (
    GrowthRecordService,
)

router = APIRouter(
    prefix="/children/{child_id}/growth-records",
    tags=["Growth Records"],
)


@router.post(
    "",
    response_model=None,
)
async def create_growth_record(
    child_id: UUID,
    request: CreateGrowthRecordRequest,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        GrowthRecordService,
        Depends(get_growth_record_service),
    ],
):
    """
    Creates a new growth record for a child.
    """

    record = await service.create_growth_record(
        child_id=child_id,
        parent_id=current_user.id,
        data=request,
    )

    return success_response(
        data=GrowthRecordResponse.model_validate(
            record,
        ),
        message="Growth record created successfully.",
    )


@router.get(
    "",
    response_model=None,
)
async def list_growth_records(
    child_id: UUID,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        GrowthRecordService,
        Depends(get_growth_record_service),
    ],
):
    """
    Returns all growth records for a child.
    """

    records = await service.list_growth_records(
        child_id=child_id,
        parent_id=current_user.id,
    )

    return success_response(
        data=[
            GrowthRecordResponse.model_validate(
                record,
            )
            for record in records
        ],
        message="Growth records retrieved successfully.",
    )


###########################################################################
# STATIC ROUTES MUST COME BEFORE /{record_id}
###########################################################################


@router.get(
    "/history",
    response_model=None,
)
async def get_growth_history(
    child_id: UUID,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        GrowthRecordService,
        Depends(get_growth_record_service),
    ],
):
    """
    Returns the complete chronological growth history.
    """

    history = await service.get_growth_history(
        child_id=child_id,
        parent_id=current_user.id,
    )

    return success_response(
        data=GrowthHistoryResponse.model_validate(
            history,
        ),
        message="Growth history retrieved successfully.",
    )


@router.get(
    "/trends",
    response_model=None,
)
async def get_growth_trends(
    child_id: UUID,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        GrowthRecordService,
        Depends(get_growth_record_service),
    ],
):
    """
    Returns longitudinal growth trends.
    """

    trends = await service.get_growth_trends(
        child_id=child_id,
        parent_id=current_user.id,
    )

    return success_response(
        data=GrowthTrendResponse.model_validate(
            trends,
        ),
        message="Growth trends retrieved successfully.",
    )


###########################################################################
# DYNAMIC ROUTES
###########################################################################


@router.get(
    "/{record_id}",
    response_model=None,
)
async def get_growth_record(
    child_id: UUID,
    record_id: UUID,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        GrowthRecordService,
        Depends(get_growth_record_service),
    ],
):
    """
    Returns a single growth record.
    """

    record = await service.get_growth_record(
        child_id=child_id,
        record_id=record_id,
        parent_id=current_user.id,
    )

    return success_response(
        data=GrowthRecordResponse.model_validate(
            record,
        ),
        message="Growth record retrieved successfully.",
    )


@router.get(
    "/{record_id}/analysis",
    response_model=None,
)
async def analyze_growth_record(
    child_id: UUID,
    record_id: UUID,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        GrowthRecordService,
        Depends(get_growth_record_service),
    ],
):
    """
    Returns WHO growth analysis.
    """

    analysis = await service.analyze_growth_record(
        child_id=child_id,
        record_id=record_id,
        parent_id=current_user.id,
    )

    return success_response(
        data=GrowthAnalysisResult.model_validate(
            analysis,
        ),
        message="Growth analysis completed successfully.",
    )


@router.put(
    "/{record_id}",
    response_model=None,
)
async def update_growth_record(
    child_id: UUID,
    record_id: UUID,
    request: UpdateGrowthRecordRequest,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        GrowthRecordService,
        Depends(get_growth_record_service),
    ],
):
    """
    Updates an existing growth record.
    """

    record = await service.update_growth_record(
        child_id=child_id,
        record_id=record_id,
        parent_id=current_user.id,
        data=request,
    )

    return success_response(
        data=GrowthRecordResponse.model_validate(
            record,
        ),
        message="Growth record updated successfully.",
    )


@router.delete(
    "/{record_id}",
    response_model=None,
)
async def delete_growth_record(
    child_id: UUID,
    record_id: UUID,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        GrowthRecordService,
        Depends(get_growth_record_service),
    ],
):
    """
    Soft deletes a growth record.
    """

    await service.delete_growth_record(
        child_id=child_id,
        record_id=record_id,
        parent_id=current_user.id,
    )

    return success_response(
        message="Growth record deleted successfully.",
    )