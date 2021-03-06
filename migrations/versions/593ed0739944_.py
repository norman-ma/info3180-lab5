"""empty message

Revision ID: 593ed0739944
Revises: d2856d6839eb
Create Date: 2017-03-06 04:55:16.454166

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '593ed0739944'
down_revision = 'd2856d6839eb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_profile', sa.Column('age', sa.Integer(), nullable=True))
    op.add_column('user_profile', sa.Column('bio', sa.Text(), nullable=True))
    op.add_column('user_profile', sa.Column('created_on', sa.DateTime(), nullable=True))
    op.add_column('user_profile', sa.Column('gender', sa.String(length=10), nullable=True))
    op.drop_column('user_profile', 'password')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_profile', sa.Column('password', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.drop_column('user_profile', 'gender')
    op.drop_column('user_profile', 'created_on')
    op.drop_column('user_profile', 'bio')
    op.drop_column('user_profile', 'age')
    # ### end Alembic commands ###
