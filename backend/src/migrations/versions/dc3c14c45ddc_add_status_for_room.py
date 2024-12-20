"""Add status for room

Revision ID: dc3c14c45ddc
Revises: 995c6c936c07
Create Date: 2024-11-13 03:21:59.004174

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'dc3c14c45ddc'
down_revision: Union[str, None] = '995c6c936c07'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_token_blacklist_token', table_name='token_blacklist')
    op.drop_table('token_blacklist')
    op.drop_table('rate_limit')
    op.add_column('room', sa.Column('from_date', sa.DateTime(timezone=True), nullable=True))
    op.add_column('room', sa.Column('to_date', sa.DateTime(timezone=True), nullable=True))
    op.add_column('room', sa.Column('status', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('room', 'status')
    op.drop_column('room', 'to_date')
    op.drop_column('room', 'from_date')
    op.create_table('rate_limit',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('path', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('limit', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('period', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='rate_limit_pkey'),
    sa.UniqueConstraint('name', name='rate_limit_name_key')
    )
    op.create_table('token_blacklist',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('token', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('expires_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='token_blacklist_pkey')
    )
    op.create_index('ix_token_blacklist_token', 'token_blacklist', ['token'], unique=True)
    # ### end Alembic commands ###
