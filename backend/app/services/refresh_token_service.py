import hashlib
import secrets
from datetime import UTC
from datetime import datetime
from datetime import timedelta
from uuid import UUID

from app.models.refresh_token import RefreshToken
from app.repositories import RefreshTokenRepository

from app.core.exceptions import AuthenticationError
from app.services.jwt_service import JWTService

class RefreshTokenService:
    """
    Handles refresh token lifecycle.
    """

    REFRESH_TOKEN_EXPIRE_DAYS = 30

    def __init__(
        self,
        repository: RefreshTokenRepository,
    ):
        self.repository = repository

    def generate_token(self) -> str:
        """
        Generate a secure random refresh token.
        """

        return secrets.token_urlsafe(64)

    def hash_token(
        self,
        token: str,
    ) -> str:
        """
        Hash a refresh token before storing it.
        """

        return hashlib.sha256(
            token.encode()
        ).hexdigest()

    async def create(
        self,
        user_id: UUID,
    ) -> str:
        """
        Creates and stores a refresh token.
        """

        raw_token = self.generate_token()

        token = RefreshToken(
            user_id=user_id,
            token_hash=self.hash_token(raw_token),
            expires_at=datetime.now(UTC)
            + timedelta(
                days=self.REFRESH_TOKEN_EXPIRE_DAYS
            ),
            revoked=False,
        )

        await self.repository.create(token)

        return raw_token

    async def validate(
        self,
        raw_token: str,
    ) -> RefreshToken | None:
        """
        Validate a refresh token.
        """

        token_hash = self.hash_token(raw_token)

        return await self.repository.get_active(
            token_hash
        )

    async def revoke(
        self,
        raw_token: str,
    ) -> None:
        """
        Revoke one refresh token.
        """

        token_hash = self.hash_token(raw_token)

        token = await self.repository.get_by_hash(
            token_hash
        )

        if token:
            await self.repository.revoke(token)

    async def revoke_all(
        self,
        user_id: UUID,
    ) -> None:
        """
        Revoke all refresh tokens for a user.
        """

        await self.repository.revoke_all_for_user(
            user_id
        )

    async def rotate(
        self,
        refresh_token: str,
    ) -> tuple[str, str]:
        """
        Rotate a refresh token.
        """

        token_hash = self.hash_token(
            refresh_token
        )

        stored = await self.repository.get_active(
            token_hash
        )

        if stored is None:
            raise AuthenticationError(
                "Invalid refresh token."
            )

        await self.repository.revoke(stored)

        jwt_service = JWTService()

        access_token = jwt_service.create_access_token(
            str(stored.user_id)
        )

        new_refresh = await self.create(
            stored.user_id
        )

        return (
            access_token,
            new_refresh,
        )