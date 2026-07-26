from datetime import UTC
from datetime import datetime
from datetime import timedelta

import jwt
from jwt import InvalidTokenError

from app.core.exceptions import AuthenticationError
from app.core.settings import settings


class JWTService:
    """
    Handles JWT creation and verification.
    """

    def create_access_token(
        self,
        subject: str,
    ) -> str:
        """
        Creates a signed JWT access token.
        """

        expires_at = datetime.now(UTC) + timedelta(
            minutes=settings.jwt_access_token_expire_minutes,
        )

        payload = {
            "sub": subject,
            "exp": expires_at,
            "iat": datetime.now(UTC),
        }

        token = jwt.encode(
            payload,
            settings.jwt_secret_key,
            algorithm=settings.jwt_algorithm,
        )

        return token

    def decode_access_token(
        self,
        token: str,
    ) -> dict:
        """
        Decodes and validates a JWT.
        """

        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret_key,
                algorithms=[
                    settings.jwt_algorithm,
                ],
            )

            return payload

        except InvalidTokenError:
            raise AuthenticationError(
                "Invalid or expired access token."
            )