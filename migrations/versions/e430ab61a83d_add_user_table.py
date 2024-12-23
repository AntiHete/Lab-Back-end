"""Add user table

Revision ID: e430ab61a83d
Revises: 789aa313519e
Create Date: 2024-12-22 19:50:06.776805

"""
from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic.
revision = 'e430ab61a83d'
down_revision = '789aa313519e'
branch_labels = None
depends_on = None


def upgrade():
    """
    Upgrade the database schema by creating the 'user' table.
    """
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment='Primary key of the user'),
        sa.Column('username', sa.String(length=80), nullable=False, comment='Unique username of the user'),
        sa.Column('password', sa.String(length=128), nullable=False, comment='Hashed password of the user'),
        sa.PrimaryKeyConstraint('id', name='pk_user_id'),
        sa.UniqueConstraint('username', name='uq_user_username')
    )

def downgrade():
    """
    Downgrade the database schema by dropping the 'user' table.
    """
    op.drop_table('user')
