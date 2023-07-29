"""migrations

Revision ID: 9d7951b5e16b
Revises: 1e78c5c70437
Create Date: 2023-07-29 16:31:48.583968

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9d7951b5e16b'
down_revision = '1e78c5c70437'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('milk_banks', sa.Column('name', sa.String(), nullable=False))
    op.alter_column('milk_banks', 'phone_number',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('milk_banks', 'email',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('milk_banks', 'email',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('milk_banks', 'phone_number',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_column('milk_banks', 'name')
    # ### end Alembic commands ###