"""updated product image model

Revision ID: 11e56bb14185
Revises: e18d8fba1c60
Create Date: 2024-08-16 11:14:57.691265

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '11e56bb14185'
down_revision = 'e18d8fba1c60'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ProductImage', schema=None) as batch_op:
        batch_op.drop_constraint('ProductImage_product_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'Products', ['product_id'], ['id'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ProductImage', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('ProductImage_product_id_fkey', 'Products', ['product_id'], ['id'])

    # ### end Alembic commands ###
