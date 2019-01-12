"""empty message

Revision ID: d30a23ad2163
Revises: 75eb11b7c89b
Create Date: 2019-01-12 21:53:04.376930

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd30a23ad2163'
down_revision = '75eb11b7c89b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'form', 'user', ['id_user'], ['id'])
    op.add_column('question', sa.Column('id_form', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'question', 'form', ['id_form'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'question', type_='foreignkey')
    op.drop_column('question', 'id_form')
    op.drop_constraint(None, 'form', type_='foreignkey')
    # ### end Alembic commands ###
