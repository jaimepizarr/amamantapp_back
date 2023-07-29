"""migrations

Revision ID: a030358c61dd
Revises: 9f99161e19df
Create Date: 2023-07-29 17:22:08.939406

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a030358c61dd'
down_revision = '9f99161e19df'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('milk_banks', sa.Column('image_url', sa.String(), nullable=True))
    op.create_index(op.f('ix_milk_banks_email'), 'milk_banks', ['email'], unique=False)
    op.create_index(op.f('ix_milk_banks_name'), 'milk_banks', ['name'], unique=False)
    op.create_index(op.f('ix_milk_banks_website'), 'milk_banks', ['website'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_milk_banks_website'), table_name='milk_banks')
    op.drop_index(op.f('ix_milk_banks_name'), table_name='milk_banks')
    op.drop_index(op.f('ix_milk_banks_email'), table_name='milk_banks')
    op.drop_column('milk_banks', 'image_url')
    # ### end Alembic commands ###
