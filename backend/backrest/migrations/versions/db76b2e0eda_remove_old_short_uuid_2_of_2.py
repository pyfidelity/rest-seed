""" remove old short uuid 1/2

Revision ID: db76b2e0eda
Revises: 4ae8cbbb5550
Create Date: 2015-07-31 15:13:23.293178

"""

# revision identifiers, used by Alembic.
revision = 'db76b2e0eda'
down_revision = '4ae8cbbb5550'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_column('principal', 'uuid')


def downgrade():
    op.add_column(
        'principal', sa.Column(
            'uuid',
            sa.VARCHAR(length=12), autoincrement=False, nullable=True))
