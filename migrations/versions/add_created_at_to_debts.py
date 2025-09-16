"""Add created_at to debts

Revision ID: add_created_at_to_debts
Revises: 
Create Date: 2025-09-16 15:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_created_at_to_debts'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('debts', sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True))


def downgrade():
    op.drop_column('debts', 'created_at')
