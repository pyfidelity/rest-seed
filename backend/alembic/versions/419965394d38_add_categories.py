""" add (groupable) categories

Revision ID: 419965394d38
Revises: 2fa92ef6570b
Create Date: 2014-09-22 16:33:46.225247

"""

# revision identifiers, used by Alembic.
revision = '419965394d38'
down_revision = '2fa92ef6570b'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('categorygroup',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.Unicode(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('category',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.Unicode(), nullable=False),
        sa.Column('group_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['group_id'], [u'categorygroup.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_category_title'), 'category', ['title'], unique=False)
    op.create_table('categories',
        sa.Column('category_id', sa.Integer(), nullable=False),
        sa.Column('content_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['category_id'], [u'category.id'], ),
        sa.ForeignKeyConstraint(['content_id'], [u'content.id'], ),
        sa.PrimaryKeyConstraint('category_id', 'content_id')
    )


def downgrade():
    op.drop_table('categories')
    op.drop_index(op.f('ix_category_title'), table_name='category')
    op.drop_table('category')
    op.drop_table('categorygroup')
