from fastapi import APIRouter

from app.api.routers import (
    auth_router,
    system_router,
    users_router,
)

router = APIRouter()

router.include_router(system_router)
router.include_router(auth_router)
router.include_router(users_router)