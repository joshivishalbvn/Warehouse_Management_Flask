"""updated barcode model

Revision ID: 86ad3c65b3c1
Revises: 1042efd63e5d
Create Date: 2024-08-16 17:05:24.229451

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '86ad3c65b3c1'
down_revision = '1042efd63e5d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Barcode', schema=None) as batch_op:
        batch_op.drop_column('code_url')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Barcode', schema=None) as batch_op:
        batch_op.add_column(sa.Column('code_url', sa.VARCHAR(), autoincrement=False, nullable=False))

    # ### end Alembic commands ###
