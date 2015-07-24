""" remove old short uuid 1/2

Revision ID: 4ae8cbbb5550
Revises: 3175f81dd541
Create Date: 2015-07-31 14:28:46.318087

"""

# revision identifiers, used by Alembic.
revision = '4ae8cbbb5550'
down_revision = '3175f81dd541'

from alembic import op
from uuid import uuid4
import sqlalchemy as sa


def table(name):
    engine = op.get_bind().engine
    metadata = sa.MetaData(engine)
    metadata.reflect(only=[name])
    return metadata.tables[name]


def uuids(length=12):
    existing = set()
    while True:
        uuid = str(uuid4()).replace('-', '')[:length]
        if uuid not in existing:
            yield uuid
        existing.add(uuid)


def upgrade():
    op.drop_index('ix_principal_uuid', table_name='principal')


def downgrade():
    op.execute('commit')
    principals = table('principal')
    ids = [p.id for p in principals.select().execute()]
    for pid in ids:
        uuid = uuids().next()
        principals.update().where(principals.c.id == pid).values(uuid=uuid).execute()
    op.alter_column('principal', 'uuid', nullable=False)
    op.create_index(op.f('ix_principal_uuid'), 'principal', ['uuid'], unique=True)
