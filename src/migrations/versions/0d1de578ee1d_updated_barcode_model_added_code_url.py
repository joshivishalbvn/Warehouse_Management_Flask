"""updated barcode model added code_url

Revision ID: 0d1de578ee1d
Revises: 86ad3c65b3c1
Create Date: 2024-08-16 17:05:39.282712

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0d1de578ee1d'
down_revision = '86ad3c65b3c1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Barcode', schema=None) as batch_op:
        batch_op.add_column(sa.Column('code_url', sa.LargeBinary(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Barcode', schema=None) as batch_op:
        batch_op.drop_column('code_url')

    # ### end Alembic commands ###
