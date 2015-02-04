""" add file uuids

Revision ID: 1e0ff2269c43
Revises: 47ecebadac41
Create Date: 2015-02-04 17:39:38.648599

"""

# revision identifiers, used by Alembic.
revision = '1e0ff2269c43'
down_revision = '47ecebadac41'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


def upgrade():
    op.add_column('file', sa.Column('uuid', postgresql.UUID(as_uuid=True)))
    op.execute('''UPDATE file SET uuid = uuid(split_part(path, '.', 1));''')
    op.alter_column('file', 'uuid', nullable=False)
    op.create_index(op.f('ix_file_uuid'), 'file', ['uuid'], unique=True)
    op.drop_constraint(u'file_path_key', 'file', type_='unique')
    op.drop_column('file', 'path')


def downgrade():
    op.add_column('file', sa.Column('path', sa.VARCHAR(length=128), autoincrement=False))
    op.execute('''UPDATE file SET path = concat(uuid, substring(filename from '\.[^.]*$'));''')
    op.alter_column('file', 'path', nullable=False)
    op.create_unique_constraint(u'file_path_key', 'file', ['path'])
    op.drop_index(op.f('ix_file_uuid'), table_name='file')
    op.drop_column('file', 'uuid')
