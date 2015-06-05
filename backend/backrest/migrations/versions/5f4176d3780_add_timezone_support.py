""" add timezone support

Revision ID: 5f4176d3780
Revises: 1e0ff2269c43
Create Date: 2015-06-05 16:02:30.552314

"""

# revision identifiers, used by Alembic.
revision = '5f4176d3780'
down_revision = '1e0ff2269c43'

from alembic import op


def upgrade():
    op.execute('''ALTER TABLE content ALTER creation_date TYPE timestamptz;''')
    op.execute('''ALTER TABLE content ALTER modification_date TYPE timestamptz;''')
    op.execute('''ALTER TABLE principal ALTER creation_date TYPE timestamptz;''')
    op.execute('''ALTER TABLE principal ALTER last_login_date TYPE timestamptz;''')


def downgrade():
    pass
