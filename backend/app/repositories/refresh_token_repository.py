from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.refresh_token import RefreshToken
from app.repositories.base import BaseRepository


class RefreshTokenRepository(BaseRepository):
    """
    Repository for refresh tokens.
    """

    def __init__(
        self,
        db: AsyncSession,
    ):
        super().__init__(
            db=db,
            model=RefreshToken,
        )

    async def create(
        self,
        token: RefreshToken,
    ) -> RefreshToken:
        self.db.add(token)
        await self.db.commit()
        await self.db.refresh(token)
        return token

    async def get_by_hash(
        self,
        token_hash: str,
    ) -> RefreshToken | None:
        result = await self.db.execute(
            select(RefreshToken).where(
                RefreshToken.token_hash == token_hash
            )
        )

        return result.scalar_one_or_none()

    async def get_active(
        self,
        token_hash: str,
    ) -> RefreshToken | None:
        result = await self.db.execute(
            select(RefreshToken).where(
                RefreshToken.token_hash == token_hash,
                RefreshToken.revoked.is_(False),
                RefreshToken.expires_at > datetime.utcnow(),
            )
        )

        return result.scalar_one_or_none()

    async def revoke(
        self,
        token: RefreshToken,
    ) -> RefreshToken:
        token.revoked = True

        await self.db.commit()
        await self.db.refresh(token)

        return token

    async def revoke_all_for_user(
        self,
        user_id: UUID,
    ) -> None:
        result = await self.db.execute(
            select(RefreshToken).where(
                RefreshToken.user_id == user_id,
                RefreshToken.revoked.is_(False),
            )
        )

        tokens = result.scalars().all()

        for token in tokens:
            token.revoked = True

        await self.db.commit()