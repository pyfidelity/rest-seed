""" add principal uuid

Revision ID: 371da29a11be
Revises: 5f4176d3780
Create Date: 2015-07-13 16:24:18.131830

"""

# revision identifiers, used by Alembic.
revision = '371da29a11be'
down_revision = '5f4176d3780'


from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('principal', sa.Column('uuid', sa.String(length=12), nullable=False))
    op.create_index(op.f('ix_principal_uuid'), 'principal', ['uuid'], unique=True)


def downgrade():
    op.drop_index(op.f('ix_principal_uuid'), table_name='principal')
    op.drop_column('principal', 'uuid')
