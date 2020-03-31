"""Add confirmed and comfirmed_date fields

Revision ID: ab7680a432e1
Revises: ab289c6a00fb
Create Date: 2020-03-31 19:37:24.795820

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab7680a432e1'
down_revision = 'ab289c6a00fb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('confirmed', sa.Boolean(), nullable=True))
    op.add_column('user', sa.Column('confirmed_date', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'confirmed_date')
    op.drop_column('user', 'confirmed')
    # ### end Alembic commands ###
