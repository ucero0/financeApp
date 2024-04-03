"""add admin column to users

Revision ID: b81099a38280
Revises: a5f34adb18d4
Create Date: 2024-03-26 17:51:26.894373

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b81099a38280'
down_revision: Union[str, None] = 'a5f34adb18d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('admin', sa.Boolean(), nullable=True))
    op.drop_constraint('users_username_key', 'users', type_='unique')
    op.drop_column('users', 'username')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('username', sa.VARCHAR(length=50), autoincrement=False, nullable=True))
    op.create_unique_constraint('users_username_key', 'users', ['username'])
    op.drop_column('users', 'admin')
    # ### end Alembic commands ###
