"""add external offer id

Revision ID: df075b6af763
Revises: 9305d95ce02e
Create Date: 2020-02-20 18:20:57.395465

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df075b6af763'
down_revision = '9305d95ce02e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('offer', sa.Column('external_offer_id', sa.Integer(), nullable=True))
    op.create_unique_constraint(None, 'offer', ['external_offer_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'offer', type_='unique')
    op.drop_column('offer', 'external_offer_id')
    # ### end Alembic commands ###
