from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('debts', sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True))


def downgrade():
    op.drop_column('debts', 'created_at')
