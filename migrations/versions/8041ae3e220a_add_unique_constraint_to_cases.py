"""Add unique constraint to cases

Revision ID: 8041ae3e220a
Revises:
Create Date: 2021-09-24 09:16:01.887307

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8041ae3e220a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_unique_constraint('uq_cases_date_state', 'case', ['date', 'state'])


def downgrade():
    op.drop_constraint('uq_cases-date_state', 'case')
