"""Add importance field

Revision ID: ab289c6a00fb
Revises: 0722d1c4d8ed
Create Date: 2020-03-31 01:53:01.476014

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab289c6a00fb'
down_revision = '0722d1c4d8ed'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('importance', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'importance')
    # ### end Alembic commands ###
