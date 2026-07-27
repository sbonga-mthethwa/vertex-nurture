from .auth import router as auth_router
from .profile import router as profile_router
from .system import router as system_router
from .users import router as users_router
from .children import router as children_router

__all__ = [
    "auth_router",
    "profile_router",
    "system_router",
    "users_router",
    "children_router",
]