"""empty message

Revision ID: 5ccdcd5a72b3
Revises: 
Create Date: 2022-04-18 12:06:12.212510

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5ccdcd5a72b3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('img2', sa.Text(), nullable=True))
    op.add_column('products', sa.Column('img3', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('products', 'img3')
    op.drop_column('products', 'img2')
    # ### end Alembic commands ###
