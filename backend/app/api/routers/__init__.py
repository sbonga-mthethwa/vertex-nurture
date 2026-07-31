from .auth import router as auth_router
from .profile import router as profile_router
from .system import router as system_router
from .users import router as users_router
from .children import router as children_router
from .growth_records import router as growth_records_router
from app.api.routers.vaccination_records import (
    router as vaccination_records_router,
)
from .vaccination_reminders import (
    router as vaccination_reminders_router,
)
from . import vaccination_reminders

from app.api.routers.devices import router as devices_router


__all__ = [
    "auth_router",
    "profile_router",
    "system_router",
    "users_router",
    "children_router",
    "growth_records_router",
    "vaccination_records_router",
    "vaccination_reminders",
    "vaccination_reminders_router",
    "devices_router",
]