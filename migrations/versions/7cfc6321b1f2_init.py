"""init

Revision ID: 7cfc6321b1f2
Revises: 
Create Date: 2024-06-10 09:57:10.168499

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7cfc6321b1f2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
    sa.Column('id', sa.Text(), nullable=False),
    sa.Column('username', sa.String(length=100), nullable=False),
    sa.Column('password', sa.Text(), nullable=False),
    sa.Column('updated_at', sa.Float(), nullable=False),
    sa.Column('created_at', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('achievement',
    sa.Column('id', sa.Text(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('year', sa.Integer(), nullable=False),
    sa.Column('photo_url', sa.String(length=100), nullable=False),
    sa.Column('created_by', sa.Text(), nullable=False),
    sa.Column('updated_at', sa.Float(), nullable=False),
    sa.Column('created_at', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['created_by'], ['admin.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('photo_url')
    )
    op.create_table('event',
    sa.Column('id', sa.Text(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('photo_url', sa.String(length=100), nullable=False),
    sa.Column('created_by', sa.Text(), nullable=False),
    sa.Column('updated_at', sa.Float(), nullable=False),
    sa.Column('created_at', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['created_by'], ['admin.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('photo_url'),
    sa.UniqueConstraint('title')
    )
    op.create_table('gallery',
    sa.Column('id', sa.Text(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('photo_url', sa.String(length=100), nullable=False),
    sa.Column('created_by', sa.Text(), nullable=False),
    sa.Column('updated_at', sa.Float(), nullable=False),
    sa.Column('created_at', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['created_by'], ['admin.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('photo_url'),
    sa.UniqueConstraint('title')
    )
    op.create_table('news',
    sa.Column('id', sa.Text(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('photo_url', sa.String(length=100), nullable=False),
    sa.Column('created_by', sa.Text(), nullable=False),
    sa.Column('updated_at', sa.Float(), nullable=False),
    sa.Column('created_at', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['created_by'], ['admin.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('photo_url'),
    sa.UniqueConstraint('title')
    )
    op.create_table('user',
    sa.Column('id', sa.Text(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('password', sa.Text(), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('phone', sa.String(length=100), nullable=False),
    sa.Column('address', sa.String(length=100), nullable=False),
    sa.Column('photo_url', sa.String(length=100), nullable=True),
    sa.Column('role_id', sa.Text(), nullable=True),
    sa.Column('role_text', sa.String(length=100), nullable=True),
    sa.Column('created_by', sa.Text(), nullable=False),
    sa.Column('updated_at', sa.Float(), nullable=False),
    sa.Column('created_at', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['created_by'], ['admin.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('address'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('phone'),
    sa.UniqueConstraint('photo_url')
    )
    op.create_table('achievement_country',
    sa.Column('id', sa.Text(), nullable=False),
    sa.Column('country', sa.String(length=100), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('updated_at', sa.Float(), nullable=False),
    sa.Column('created_at', sa.Float(), nullable=False),
    sa.Column('achievement_id', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['achievement_id'], ['achievement.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('country'),
    sa.UniqueConstraint('title')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('achievement_country')
    op.drop_table('user')
    op.drop_table('news')
    op.drop_table('gallery')
    op.drop_table('event')
    op.drop_table('achievement')
    op.drop_table('admin')
    # ### end Alembic commands ###