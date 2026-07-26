from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi import Depends

from app.api.responses import success_response
from app.dependencies import get_current_user
from app.dependencies.services import (
    get_authentication_service,
    get_refresh_token_service,
)
from app.schemas.auth import (
    LoginResponse,
    RefreshRequest,
    TokenResponse,
)
from app.schemas.user import (
    CreateUserRequest,
    LoginRequest,
    UserResponse,
)
from app.services.authentication_service import (
    AuthenticationService,
)
from app.services.refresh_token_service import (
    RefreshTokenService,
)

from app.schemas.auth import LogoutRequest
from app.models.user import User

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/register")
async def register(
    request: CreateUserRequest,
    service: Annotated[
        AuthenticationService,
        Depends(get_authentication_service),
    ],
):
    """
    Register a new user.
    """

    user = await service.register(
        email=request.email,
        full_name=request.full_name,
        password=request.password,
    )

    return success_response(
        data=UserResponse.model_validate(user),
        message="User registered successfully.",
    )


@router.post("/login")
async def login(
    request: LoginRequest,
    service: Annotated[
        AuthenticationService,
        Depends(get_authentication_service),
    ],
):
    """
    Authenticate a user.
    """

    access_token, refresh_token = await service.login(
        email=request.email,
        password=request.password,
    )

    return success_response(
        data=LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
        ),
        message="Login successful.",
    )


@router.post("/refresh")
async def refresh(
    request: RefreshRequest,
    service: Annotated[
        RefreshTokenService,
        Depends(get_refresh_token_service),
    ],
):
    """
    Refresh an access token.
    """

    access_token, refresh_token = await service.rotate(
        request.refresh_token,
    )

    return success_response(
        data=TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="Bearer",
        ),
        message="Token refreshed successfully.",
    )


@router.post("/logout")
async def logout(
    request: LogoutRequest,
    service: Annotated[
        AuthenticationService,
        Depends(get_authentication_service),
    ],
):
    """
    Logout the current session.
    """

    await service.logout(
        request.refresh_token
    )

    return success_response(
        message="Logged out successfully.",
    )


@router.get("/me")
async def me(
    current_user=Depends(get_current_user),
):
    """
    Returns the currently authenticated user.
    """

    return success_response(
        data=UserResponse.model_validate(current_user),
        message="Authenticated user retrieved.",
    )


@router.post("/logout-all")
async def logout_all(
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        AuthenticationService,
        Depends(get_authentication_service),
    ],
):
    """
    Logout from all devices.
    """

    await service.logout_all(
        current_user.id
    )

    return success_response(
        message="Logged out from all devices.",
    )