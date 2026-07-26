"""add user roles

Revision ID: 4a62047655ed
Revises: e9435e9a2403
Create Date: 2026-07-26 19:02:22.733724

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "4a62047655ed"
down_revision: Union[str, Sequence[str], None] = "e9435e9a2403"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Remove default from refresh_tokens.revoked
    op.alter_column(
        "refresh_tokens",
        "revoked",
        existing_type=sa.BOOLEAN(),
        server_default=None,
        existing_nullable=False,
    )

    # Create PostgreSQL enum type
    user_role = postgresql.ENUM(
        "USER",
        "ADMIN",
        "SUPER_ADMIN",
        name="userrole",
    )

    user_role.create(
        op.get_bind(),
        checkfirst=True,
    )

    # Add role column with temporary default
    op.add_column(
        "users",
        sa.Column(
            "role",
            user_role,
            nullable=False,
            server_default="USER",
        ),
    )

    # Remove temporary default
    op.alter_column(
        "users",
        "role",
        server_default=None,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column(
        "users",
        "role",
    )

    user_role = postgresql.ENUM(
        "USER",
        "ADMIN",
        "SUPER_ADMIN",
        name="userrole",
    )

    user_role.drop(
        op.get_bind(),
        checkfirst=True,
    )

    op.alter_column(
        "refresh_tokens",
        "revoked",
        existing_type=sa.BOOLEAN(),
        server_default=sa.text("false"),
        existing_nullable=False,
    )