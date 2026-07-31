"""create vaccination reminders table

Revision ID: 21016a5ba037
Revises: 8d3d7d2b2d91
Create Date: 2026-07-30

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "21016a5ba037"
down_revision: Union[str, Sequence[str], None] = "8d3d7d2b2d91"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


reminder_type_enum = postgresql.ENUM(
    "30_DAYS",
    "14_DAYS",
    "7_DAYS",
    "1_DAY",
    "DUE_TODAY",
    "OVERDUE",
    name="remindertype",
    create_type=False,
)

reminder_status_enum = postgresql.ENUM(
    "PENDING",
    "SENT",
    "DISMISSED",
    name="reminderstatus",
    create_type=False,
)

reminder_channel_enum = postgresql.ENUM(
    "PUSH",
    "EMAIL",
    "SMS",
    name="reminderchannel",
    create_type=False,
)


def upgrade() -> None:
    """
    Upgrade schema.
    """

    bind = op.get_bind()

    reminder_type_enum.create(bind, checkfirst=True)
    reminder_status_enum.create(bind, checkfirst=True)
    reminder_channel_enum.create(bind, checkfirst=True)

    op.create_table(
        "vaccination_reminders",

        sa.Column(
            "child_id",
            sa.UUID(),
            nullable=False,
        ),

        sa.Column(
            "vaccination_record_id",
            sa.UUID(),
            nullable=True,
        ),

        sa.Column(
            "vaccine_name",
            sa.String(length=150),
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
            "reminder_date",
            sa.Date(),
            nullable=False,
        ),

        sa.Column(
            "reminder_type",
            reminder_type_enum,
            nullable=False,
        ),

        sa.Column(
            "status",
            reminder_status_enum,
            nullable=False,
            server_default=sa.text("'PENDING'"),
        ),

        sa.Column(
            "channel",
            reminder_channel_enum,
            nullable=False,
            server_default=sa.text("'PUSH'"),
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
            sa.DateTime(timezone=True),
            nullable=False,
        ),

        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),

        sa.ForeignKeyConstraint(
            ["child_id"],
            ["children.id"],
            ondelete="CASCADE",
        ),

        sa.ForeignKeyConstraint(
            ["vaccination_record_id"],
            ["vaccination_records.id"],
            ondelete="SET NULL",
        ),

        sa.PrimaryKeyConstraint(
            "id",
        ),
    )

    op.create_index(
        op.f(
            "ix_vaccination_reminders_child_id",
        ),
        "vaccination_reminders",
        ["child_id"],
        unique=False,
    )

    op.create_index(
        op.f(
            "ix_vaccination_reminders_vaccination_record_id",
        ),
        "vaccination_reminders",
        ["vaccination_record_id"],
        unique=False,
    )

    op.create_index(
        "ix_vaccination_reminder_date",
        "vaccination_reminders",
        ["reminder_date"],
        unique=False,
    )


def downgrade() -> None:
    """
    Downgrade schema.
    """

    bind = op.get_bind()

    op.drop_index(
        "ix_vaccination_reminder_date",
        table_name="vaccination_reminders",
    )

    op.drop_index(
        op.f(
            "ix_vaccination_reminders_vaccination_record_id",
        ),
        table_name="vaccination_reminders",
    )

    op.drop_index(
        op.f(
            "ix_vaccination_reminders_child_id",
        ),
        table_name="vaccination_reminders",
    )

    op.drop_table(
        "vaccination_reminders",
    )

    reminder_channel_enum.drop(bind, checkfirst=True)
    reminder_status_enum.drop(bind, checkfirst=True)
    reminder_type_enum.drop(bind, checkfirst=True)