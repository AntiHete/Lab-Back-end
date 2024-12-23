"""Initial migration

Revision ID: 789aa313519e
Revises: 
Create Date: 2024-12-22 19:38:04.072947

"""
from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic.
revision = '789aa313519e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """
    Upgrade the database schema by creating the 'accounts' table.
    """
    op.create_table(
        'accounts',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment='Primary key of the account'),
        sa.Column('user_id', sa.Integer(), nullable=False, comment='Reference to the user owning the account'),
        sa.Column('balance', sa.Float(precision=2), nullable=False, comment='Current balance of the account'),
        sa.PrimaryKeyConstraint('id', name='pk_accounts_id'),
        sa.UniqueConstraint('user_id', name='uq_accounts_user_id')
    )
    
def downgrade():
    """
    Downgrade the database schema by dropping the 'accounts' table.
    """
    op.drop_table('accounts')

