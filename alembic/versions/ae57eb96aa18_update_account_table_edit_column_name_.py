"""update account table edit column name to username

Revision ID: ae57eb96aa18
Revises: c5625edae583
Create Date: 2023-10-25 01:23:41.533183

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "ae57eb96aa18"
down_revision: Union[str, None] = "c5625edae583"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("accounts", "name", new_column_name="username")


def downgrade() -> None:
    op.alter_column("accounts", "username", new_column_name="name")
