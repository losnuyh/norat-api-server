"""create auth phone table

Revision ID: 0001
Revises:
Create Date: 2023-12-25 20:00:05.051515

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "auth_phone",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(length=20), nullable=False),
        sa.Column("expired_at", sa.DateTime(), nullable=False),
        sa.Column("phone", sa.String(length=20), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_auth_phone_code"), "auth_phone", ["code"], unique=False)
    op.create_index(op.f("ix_auth_phone_phone"), "auth_phone", ["phone"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_auth_phone_phone"), table_name="auth_phone")
    op.drop_index(op.f("ix_auth_phone_code"), table_name="auth_phone")
    op.drop_table("auth_phone")
    # ### end Alembic commands ###
