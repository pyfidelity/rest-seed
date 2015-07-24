""" from integer principal id to uuid 2/2

Revision ID: 3175f81dd541
Revises: 106bcc7ccb40
Create Date: 2015-07-31 14:23:56.569151

"""

# revision identifiers, used by Alembic.
revision = '3175f81dd541'
down_revision = '106bcc7ccb40'

from alembic import op
from uuid import uuid4
import sqlalchemy as sa


def table(name):
    engine = op.get_bind().engine
    metadata = sa.MetaData(engine)
    metadata.reflect(only=[name])
    return metadata.tables[name]


def uuids():
    existing = set()
    while True:
        uuid = str(uuid4())
        short_uuid = uuid.replace('-', '')[:8]
        if short_uuid not in existing:
            existing.add(short_uuid)
            yield uuid


def upgrade():
    op.execute('commit')
    principal = table('principal')
    globalroles = table('globalroles')
    ids = [p.id for p in principal.select().execute()]
    for pid in ids:
        uuid = uuids().next()
        principal.update().where(principal.c.id == pid).values(_tmp_id=uuid).execute()
        globalroles.update().where(globalroles.c.principal_id == pid).values(_tmp_principal_id=uuid).execute()
    op.drop_constraint('globalroles_principal_id_fkey', 'globalroles', type_='foreignkey')
    op.drop_column('globalroles', 'principal_id')
    op.drop_column('principal', 'id')
    op.alter_column('globalroles', '_tmp_principal_id', new_column_name='principal_id', nullable=False)
    op.alter_column('principal', '_tmp_id', new_column_name='id', nullable=False)
    op.create_primary_key("principal_pkey", "principal", ["id"])
    op.create_primary_key("globalroles_pkey", "globalroles", ["principal_id", "role"])
    op.create_foreign_key(u'globalroles_principal_id_fkey', 'globalroles', 'principal', ['principal_id'], ['id'])
    op.create_index(
        'ix_unique_short_uuid', 'principal',
        [sa.text(u'substring(CAST(id AS text), 1, 8)')],
        unique=True)


def downgrade():
    op.add_column('principal', sa.Column('_tmp_id', sa.Integer()))
    op.add_column('globalroles', sa.Column('_tmp_principal_id', sa.Integer()))
