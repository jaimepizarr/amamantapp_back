"""migrations

Revision ID: 279d71ca1ab5
Revises: 3cbb01f220e0
Create Date: 2023-08-06 21:46:43.274862

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '279d71ca1ab5'
down_revision = '3cbb01f220e0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('surveys', sa.Column('survey', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('surveys', 'survey')
    # ### end Alembic commands ###
