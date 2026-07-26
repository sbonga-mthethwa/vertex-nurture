from .auth import router as auth_router
from .system import router as system_router
from .users import router as users_router

__all__ = [
    "auth_router",
    "system_router",
    "users_router",
]