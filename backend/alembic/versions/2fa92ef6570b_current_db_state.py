""" add current db state

Revision ID: 2fa92ef6570b
Revises: 411ac9c908e2
Create Date: 2013-09-16 13:24:47.579179

"""

# revision identifiers, used by Alembic.
revision = '2fa92ef6570b'
down_revision = '411ac9c908e2'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('file',
    sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('path', sa.String(length=128), nullable=False),
        sa.Column('filename', sa.Unicode(), nullable=True),
        sa.Column('mimetype', sa.String(), nullable=True),
        sa.Column('size', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('path')
    )
    op.create_table('content',
    sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('type', sa.String(length=30), nullable=False),
        sa.Column('owner', sa.Unicode(), nullable=True),
        sa.Column('title', sa.Unicode(), nullable=True),
        sa.Column('description', sa.UnicodeText(), nullable=True),
        sa.Column('creation_date', sa.DateTime(), nullable=False),
        sa.Column('modification_date', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('principal',
    sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('active', sa.Boolean(), nullable=True),
        sa.Column('email', sa.Unicode(length=100), nullable=False),
        sa.Column('password', sa.Unicode(length=100), nullable=True),
        sa.Column('firstname', sa.Unicode(), nullable=True),
        sa.Column('lastname', sa.Unicode(), nullable=True),
        sa.Column('creation_date', sa.DateTime(), nullable=False),
        sa.Column('last_login_date', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )


def downgrade():
    op.drop_table('principal')
    op.drop_table('content')
    op.drop_table('file')
