""" change file size type

Revision ID: 47ecebadac41
Revises: 451c2fd3c3d6
Create Date: 2014-11-26 13:55:55.896593

"""

# revision identifiers, used by Alembic.
revision = '47ecebadac41'
down_revision = '451c2fd3c3d6'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column('file', 'size', type_=sa.BigInteger())


def downgrade():
    op.alter_column('file', 'size', type_=sa.Integer())
