"""create vaccination records table

Revision ID: 8d3d7d2b2d91
Revises: 7bf02b5e8da3
Create Date: 2026-07-29

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8d3d7d2b2d91"
down_revision: Union[str, Sequence[str], None] = "7bf02b5e8da3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Upgrade schema.
    """

    op.create_table(
        "vaccination_records",

        sa.Column(
            "child_id",
            sa.UUID(),
            nullable=False,
        ),

        sa.Column(
            "vaccine_name",
            sa.String(
                length=200,
            ),
            nullable=False,
        ),

        sa.Column(
            "dose_number",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "scheduled_date",
            sa.Date(),
            nullable=False,
        ),

        sa.Column(
            "administered_date",
            sa.Date(),
            nullable=True,
        ),

        sa.Column(
            "batch_number",
            sa.String(
                length=100,
            ),
            nullable=True,
        ),

        sa.Column(
            "facility_name",
            sa.String(
                length=255,
            ),
            nullable=True,
        ),

        sa.Column(
            "healthcare_provider",
            sa.String(
                length=255,
            ),
            nullable=True,
        ),

        sa.Column(
            "notes",
            sa.String(
                length=1000,
            ),
            nullable=True,
        ),

        sa.Column(
            "is_administered",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),

        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),

        sa.Column(
            "id",
            sa.UUID(),
            nullable=False,
        ),

        sa.Column(
            "created_at",
            sa.DateTime(
                timezone=True,
            ),
            nullable=False,
        ),

        sa.Column(
            "updated_at",
            sa.DateTime(
                timezone=True,
            ),
            nullable=False,
        ),

        sa.ForeignKeyConstraint(
            ["child_id"],
            ["children.id"],
            ondelete="CASCADE",
        ),

        sa.PrimaryKeyConstraint(
            "id",
        ),
    )

    op.create_index(
        op.f(
            "ix_vaccination_records_child_id",
        ),
        "vaccination_records",
        ["child_id"],
        unique=False,
    )

    op.create_index(
        "ix_vaccination_child_schedule",
        "vaccination_records",
        [
            "child_id",
            "scheduled_date",
        ],
        unique=False,
    )

    op.create_index(
        "ix_vaccination_child_administered",
        "vaccination_records",
        [
            "child_id",
            "administered_date",
        ],
        unique=False,
    )


def downgrade() -> None:
    """
    Downgrade schema.
    """

    op.drop_index(
        "ix_vaccination_child_administered",
        table_name="vaccination_records",
    )

    op.drop_index(
        "ix_vaccination_child_schedule",
        table_name="vaccination_records",
    )

    op.drop_index(
        op.f(
            "ix_vaccination_records_child_id",
        ),
        table_name="vaccination_records",
    )

    op.drop_table(
        "vaccination_records",
    )