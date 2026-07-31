from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends

from app.api.responses import success_response
from app.dependencies.security import get_current_user
from app.dependencies.services import (
    get_vaccination_record_service,
)
from app.models.user import User
from app.schemas.vaccination_analysis import (
    VaccinationAnalysisResponse,
)
from app.schemas.vaccination_record import (
    CreateVaccinationRecordRequest,
    UpdateVaccinationRecordRequest,
    VaccinationRecordResponse,
)
from app.services.vaccination_record_service import (
    VaccinationRecordService,
)

from app.schemas.vaccination_forecast import (
    VaccinationForecastResponse,
)


router = APIRouter(
    prefix="/children/{child_id}/vaccination-records",
    tags=["Vaccination Records"],
)


@router.post(
    "",
    response_model=None,
)
async def create_vaccination_record(
    child_id: UUID,
    request: CreateVaccinationRecordRequest,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        VaccinationRecordService,
        Depends(get_vaccination_record_service),
    ],
):
    """
    Creates a vaccination record.
    """

    record = await service.create_vaccination_record(
        child_id=child_id,
        parent_id=current_user.id,
        data=request,
    )

    return success_response(
        data=VaccinationRecordResponse.model_validate(
            record,
        ),
        message="Vaccination record created successfully.",
    )


@router.get(
    "",
    response_model=None,
)
async def list_vaccination_records(
    child_id: UUID,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        VaccinationRecordService,
        Depends(get_vaccination_record_service),
    ],
):
    """
    Returns all vaccination records.
    """

    records = await service.list_vaccination_records(
        child_id=child_id,
        parent_id=current_user.id,
    )

    return success_response(
        data=[
            VaccinationRecordResponse.model_validate(
                record,
            )
            for record in records
        ],
        message="Vaccination records retrieved successfully.",
    )


###########################################################################
# STATIC ROUTES
###########################################################################


@router.get(
    "/upcoming",
    response_model=None,
)
async def get_upcoming_vaccinations(
    child_id: UUID,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        VaccinationRecordService,
        Depends(get_vaccination_record_service),
    ],
):
    """
    Returns upcoming vaccinations.
    """

    records = await service.get_upcoming_vaccinations(
        child_id=child_id,
        parent_id=current_user.id,
    )

    return success_response(
        data=[
            VaccinationRecordResponse.model_validate(
                record,
            )
            for record in records
        ],
        message="Upcoming vaccinations retrieved successfully.",
    )


@router.get(
    "/analysis",
    response_model=None,
)
async def get_vaccination_analysis(
    child_id: UUID,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        VaccinationRecordService,
        Depends(get_vaccination_record_service),
    ],
):
    """
    Returns a complete vaccination analysis for the child.
    """

    analysis = await service.get_vaccination_analysis(
        child_id=child_id,
        parent_id=current_user.id,
    )

    return success_response(
        data=VaccinationAnalysisResponse.model_validate(
            analysis,
        ),
        message="Vaccination analysis retrieved successfully.",
    )


@router.get(
    "/forecast",
    response_model=None,
)
async def get_vaccination_forecast(
    child_id: UUID,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        VaccinationRecordService,
        Depends(get_vaccination_record_service),
    ],
):
    """
    Returns the child's vaccination forecast.
    """

    forecast = await service.get_vaccination_forecast(
        child_id=child_id,
        parent_id=current_user.id,
    )

    return success_response(
        data=VaccinationForecastResponse.model_validate(
            forecast,
        ),
        message="Vaccination forecast retrieved successfully.",
    )

###########################################################################
# DYNAMIC ROUTES
###########################################################################


@router.get(
    "/{record_id}",
    response_model=None,
)
async def get_vaccination_record(
    child_id: UUID,
    record_id: UUID,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        VaccinationRecordService,
        Depends(get_vaccination_record_service),
    ],
):
    """
    Returns a vaccination record.
    """

    record = await service.get_vaccination_record(
        child_id=child_id,
        record_id=record_id,
        parent_id=current_user.id,
    )

    return success_response(
        data=VaccinationRecordResponse.model_validate(
            record,
        ),
        message="Vaccination record retrieved successfully.",
    )


@router.put(
    "/{record_id}",
    response_model=None,
)
async def update_vaccination_record(
    child_id: UUID,
    record_id: UUID,
    request: UpdateVaccinationRecordRequest,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        VaccinationRecordService,
        Depends(get_vaccination_record_service),
    ],
):
    """
    Updates a vaccination record.
    """

    record = await service.update_vaccination_record(
        child_id=child_id,
        record_id=record_id,
        parent_id=current_user.id,
        data=request,
    )

    return success_response(
        data=VaccinationRecordResponse.model_validate(
            record,
        ),
        message="Vaccination record updated successfully.",
    )


@router.delete(
    "/{record_id}",
    response_model=None,
)
async def delete_vaccination_record(
    child_id: UUID,
    record_id: UUID,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        VaccinationRecordService,
        Depends(get_vaccination_record_service),
    ],
):
    """
    Soft deletes a vaccination record.
    """

    await service.delete_vaccination_record(
        child_id=child_id,
        record_id=record_id,
        parent_id=current_user.id,
    )

    return success_response(
        message="Vaccination record deleted successfully.",
    )
