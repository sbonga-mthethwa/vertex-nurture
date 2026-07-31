from fastapi import APIRouter

from app.api.routers import (
    auth_router,
    children_router,
    growth_records_router,
    profile_router,
    system_router,
    users_router,
    vaccination_records_router,
    vaccination_reminders_router,
    devices_router,
)

router = APIRouter()

router.include_router(system_router)
router.include_router(auth_router)
router.include_router(users_router)
router.include_router(profile_router)
router.include_router(children_router)
router.include_router(growth_records_router)
router.include_router(vaccination_records_router)
router.include_router(vaccination_reminders_router)
router.include_router(devices_router)