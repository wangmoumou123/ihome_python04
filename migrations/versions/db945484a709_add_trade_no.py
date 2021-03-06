"""add_trade_no

Revision ID: db945484a709
Revises: fb16ea1bad64
Create Date: 2020-04-30 15:30:46.018578

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db945484a709'
down_revision = 'fb16ea1bad64'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ih_order_info', sa.Column('comment', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('ih_order_info', 'comment')
    # ### end Alembic commands ###
