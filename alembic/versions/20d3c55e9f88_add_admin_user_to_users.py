"""add admin user to users

Revision ID: 20d3c55e9f88
Revises: b81099a38280
Create Date: 2024-03-26 18:22:15.926368

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from app.core.config import dbSettings
from app.utils import auth


# revision identifiers, used by Alembic.
revision: str = '20d3c55e9f88'
down_revision: Union[str, None] = 'b81099a38280'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    hashed_password = auth.get_password_hash(dbSettings.db_password)
    op.execute(f"INSERT INTO users (email, password, admin) VALUES ('{dbSettings.db_username}@gmail.com', '{hashed_password}', true);")

def downgrade() -> None:
    op.execute(f"DELETE FROM users WHERE email = '{dbSettings.db_username}'")

