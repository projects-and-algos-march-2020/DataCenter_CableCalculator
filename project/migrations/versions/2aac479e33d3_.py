"""empty message

Revision ID: 2aac479e33d3
Revises: d837725e47da
Create Date: 2020-03-15 19:52:00.975059

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2aac479e33d3'
down_revision = 'd837725e47da'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('daily_work_fibers', sa.Column('number_cable', sa.String(length=45), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('daily_work_fibers', 'number_cable')
    # ### end Alembic commands ###
