""" from integer principal id to uuid 1/2

Revision ID: 106bcc7ccb40
Revises: 371da29a11be
Create Date: 2015-07-31 14:14:49.256005

"""

# revision identifiers, used by Alembic.
revision = '106bcc7ccb40'
down_revision = '371da29a11be'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


def table(name):
    engine = op.get_bind().engine
    metadata = sa.MetaData(engine)
    metadata.reflect(only=[name])
    return metadata.tables[name]


def upgrade():
    op.add_column('principal', sa.Column('_tmp_id', postgresql.UUID()))
    op.add_column('globalroles', sa.Column('_tmp_principal_id', postgresql.UUID()))


def downgrade():
    op.execute('commit')
    op.drop_index('ix_unique_short_uuid', table_name='principal')
    principal = table('principal')
    globalroles = table('globalroles')
    ids = [p.id for p in principal.select().execute()]
    for index, pid in enumerate(ids):
        principal.update().where(principal.c.id == pid).values(_tmp_id=index).execute()
        globalroles.update().where(globalroles.c.principal_id == pid).values(_tmp_principal_id=index).execute()
    op.drop_constraint('globalroles_principal_id_fkey', 'globalroles', type_='foreignkey')
    op.drop_column('globalroles', 'principal_id')
    op.drop_column('principal', 'id')
    op.alter_column('globalroles', '_tmp_principal_id', new_column_name='principal_id', nullable=False)
    op.alter_column('principal', '_tmp_id', new_column_name='id', nullable=False)
    op.create_primary_key("principal_pkey", "principal", ["id"])
    op.create_primary_key("globalroles_pkey", "globalroles", ["principal_id", "role"])
    op.create_foreign_key(u'globalroles_principal_id_fkey', 'globalroles', 'principal', ['principal_id'], ['id'])
