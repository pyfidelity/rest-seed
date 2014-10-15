""" add global user roles

Revision ID: 451c2fd3c3d6
Revises: 419965394d38
Create Date: 2013-11-01 00:37:32.666954

"""

# revision identifiers, used by Alembic.
revision = '451c2fd3c3d6'
down_revision = '419965394d38'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('globalroles',
        sa.Column('principal_id', sa.Integer(), nullable=False),
        sa.Column('role', sa.Unicode(), nullable=False),
        sa.ForeignKeyConstraint(['principal_id'], ['principal.id'], ),
        sa.PrimaryKeyConstraint('principal_id', 'role')
    )


def downgrade():
    op.drop_table('globalroles')
