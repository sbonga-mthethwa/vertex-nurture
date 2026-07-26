from uuid import uuid4

from app.core.exceptions import (
    AuthenticationError,
    ConflictError,
)
from app.models.user import User, UserRole
from app.repositories import UserRepository
from app.services.password_service import PasswordService
from app.services.jwt_service import JWTService
from app.services.refresh_token_service import RefreshTokenService


class AuthenticationService:
    """
    Handles user authentication.
    """

    def __init__(
        self,
        repository: UserRepository,
        refresh_token_service: RefreshTokenService,
    ):
        self.repository = repository
        self.password_service = PasswordService()
        self.jwt_service = JWTService()
        self.refresh_token_service = refresh_token_service

    async def register(
        self,
        email: str,
        full_name: str,
        password: str,
    ) -> User:
        existing = await self.repository.get_by_email(email)

        if existing:
            raise ConflictError(
                "A user with this email already exists."
            )

        password_hash = self.password_service.hash_password(password)

        user = User(
            id=uuid4(),
            email=email,
            full_name=full_name,
            password_hash=password_hash,
            is_active=True,
            role=UserRole.USER,
        )

        return await self.repository.create(user)

    async def login(
        self,
        email: str,
        password: str,
    ) -> tuple[str, str]:
        """
        Authenticate a user.
        """

        user = await self.repository.get_by_email(email)

        if user is None:
            raise AuthenticationError(
                "Invalid email or password."
            )

        if not self.password_service.verify_password(
            password,
            user.password_hash,
        ):
            raise AuthenticationError(
                "Invalid email or password."
            )

        access_token = self.jwt_service.create_access_token(
            str(user.id)
        )

        refresh_token = await self.refresh_token_service.create(
            user.id
        )

        return (
            access_token,
            refresh_token,
        )

    async def logout(
        self,
        refresh_token: str,
    ) -> None:
        """
        Logout the current session.
        """

        await self.refresh_token_service.revoke(
            refresh_token
        )

    async def logout_all(
        self,
        user_id,
    ) -> None:
        """
        Logout all active sessions.
        """

        await self.refresh_token_service.revoke_all(
            user_id
        )