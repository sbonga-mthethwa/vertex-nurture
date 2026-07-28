"""create growth records table

Revision ID: 7bf02b5e8da3
Revises: a34b324f61d1
Create Date: 2026-07-27 23:23:16.153553

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7bf02b5e8da3"
down_revision: Union[str, Sequence[str], None] = "a34b324f61d1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Upgrade schema.
    """

    op.create_table(
        "growth_records",
        sa.Column(
            "child_id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "measurement_date",
            sa.Date(),
            nullable=False,
        ),
        sa.Column(
            "age_in_months",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "weight_kg",
            sa.Numeric(
                precision=5,
                scale=2,
            ),
            nullable=False,
        ),
        sa.Column(
            "height_cm",
            sa.Numeric(
                precision=5,
                scale=2,
            ),
            nullable=False,
        ),
        sa.Column(
            "head_circumference_cm",
            sa.Numeric(
                precision=5,
                scale=2,
            ),
            nullable=True,
        ),
        sa.Column(
            "bmi",
            sa.Numeric(
                precision=5,
                scale=2,
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
        op.f("ix_growth_records_child_id"),
        "growth_records",
        ["child_id"],
        unique=False,
    )

    op.create_index(
        "ix_growth_records_child_date",
        "growth_records",
        [
            "child_id",
            "measurement_date",
        ],
        unique=False,
    )


def downgrade() -> None:
    """
    Downgrade schema.
    """

    op.drop_index(
        "ix_growth_records_child_date",
        table_name="growth_records",
    )

    op.drop_index(
        op.f("ix_growth_records_child_id"),
        table_name="growth_records",
    )

    op.drop_table(
        "growth_records",
    )