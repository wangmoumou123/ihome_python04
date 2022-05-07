"""rm_trade_no

Revision ID: 3c908c88aee1
Revises: db945484a709
Create Date: 2020-04-30 17:14:09.131699

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '3c908c88aee1'
down_revision = 'db945484a709'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('ih_order_info', 'trade_no')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ih_order_info', sa.Column('trade_no', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
