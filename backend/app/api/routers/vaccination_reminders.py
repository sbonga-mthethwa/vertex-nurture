from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends

from app.api.responses import success_response
from app.dependencies.security import get_current_user
from app.dependencies.services import (
    get_vaccination_reminder_service,
)
from app.models.user import User
from app.schemas.vaccination_reminder import (
    VaccinationReminderResponse,
)
from app.services.vaccination_reminder_service import (
    VaccinationReminderService,
)

router = APIRouter(
    prefix="/children/{child_id}/vaccination-reminders",
    tags=["Vaccination Reminders"],
)


@router.post(
    "/generate",
    response_model=None,
)
async def generate_vaccination_reminders(
    child_id: UUID,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        VaccinationReminderService,
        Depends(get_vaccination_reminder_service),
    ],
):
    """
    Generates vaccination reminders for a child.
    """

    reminders = await service.generate_reminders(
        child_id=child_id,
        parent_id=current_user.id,
    )

    return success_response(
        data=[
            VaccinationReminderResponse.model_validate(
                reminder,
            )
            for reminder in reminders
        ],
        message="Vaccination reminders generated successfully.",
    )


@router.get(
    "",
    response_model=None,
)
async def list_vaccination_reminders(
    child_id: UUID,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        VaccinationReminderService,
        Depends(get_vaccination_reminder_service),
    ],
):
    """
    Returns all reminders for a child.
    """

    reminders = await service.list_child_reminders(
        child_id=child_id,
        parent_id=current_user.id,
    )

    return success_response(
        data=[
            VaccinationReminderResponse.model_validate(
                reminder,
            )
            for reminder in reminders
        ],
        message="Vaccination reminders retrieved successfully.",
    )


###########################################################################
# STATIC ROUTES
###########################################################################


@router.get(
    "/pending",
    response_model=None,
)
async def list_pending_vaccination_reminders(
    child_id: UUID,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        VaccinationReminderService,
        Depends(get_vaccination_reminder_service),
    ],
):
    """
    Returns pending reminders.
    """

    reminders = await service.list_pending_reminders(
        child_id=child_id,
        parent_id=current_user.id,
    )

    return success_response(
        data=[
            VaccinationReminderResponse.model_validate(
                reminder,
            )
            for reminder in reminders
        ],
        message="Pending vaccination reminders retrieved successfully.",
    )


###########################################################################
# DYNAMIC ROUTES
###########################################################################


@router.get(
    "/{reminder_id}",
    response_model=None,
)
async def get_vaccination_reminder(
    child_id: UUID,
    reminder_id: UUID,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        VaccinationReminderService,
        Depends(get_vaccination_reminder_service),
    ],
):
    """
    Returns a vaccination reminder.
    """

    reminder = await service.get_reminder(
        reminder_id=reminder_id,
    )

    return success_response(
        data=VaccinationReminderResponse.model_validate(
            reminder,
        ),
        message="Vaccination reminder retrieved successfully.",
    )


@router.patch(
    "/{reminder_id}/sent",
    response_model=None,
)
async def mark_vaccination_reminder_sent(
    child_id: UUID,
    reminder_id: UUID,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        VaccinationReminderService,
        Depends(get_vaccination_reminder_service),
    ],
):
    """
    Marks a reminder as sent.
    """

    reminder = await service.mark_sent(
        reminder_id=reminder_id,
    )

    return success_response(
        data=VaccinationReminderResponse.model_validate(
            reminder,
        ),
        message="Vaccination reminder marked as sent.",
    )


@router.patch(
    "/{reminder_id}/dismiss",
    response_model=None,
)
async def dismiss_vaccination_reminder(
    child_id: UUID,
    reminder_id: UUID,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        VaccinationReminderService,
        Depends(get_vaccination_reminder_service),
    ],
):
    """
    Dismisses a reminder.
    """

    reminder = await service.dismiss_reminder(
        reminder_id=reminder_id,
    )

    return success_response(
        data=VaccinationReminderResponse.model_validate(
            reminder,
        ),
        message="Vaccination reminder dismissed successfully.",
    )


@router.delete(
    "/{reminder_id}",
    response_model=None,
)
async def delete_vaccination_reminder(
    child_id: UUID,
    reminder_id: UUID,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        VaccinationReminderService,
        Depends(get_vaccination_reminder_service),
    ],
):
    """
    Soft deletes a reminder.
    """

    await service.delete_reminder(
        reminder_id=reminder_id,
    )

    return success_response(
        message="Vaccination reminder deleted successfully.",
    )