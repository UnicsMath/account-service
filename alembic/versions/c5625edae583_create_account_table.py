"""create account table

Revision ID: c5625edae583
Revises: 
Create Date: 2023-10-24 18:45:49.108247

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c5625edae583"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "accounts",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("email", sa.String(100), nullable=False),
        sa.Column("hashed_passcode", sa.String(1024), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("accounts")
