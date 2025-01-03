"""created customers models

Revision ID: e844d2a4213e
Revises: aa28f0aeea6d
Create Date: 2024-08-22 10:39:13.544508

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e844d2a4213e'
down_revision = 'aa28f0aeea6d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Customer',
    sa.Column('status', sa.String(length=20), nullable=True),
    sa.Column('type', sa.String(length=50), nullable=True),
    sa.Column('bill_to', sa.String(length=50), nullable=True),
    sa.Column('ship_to', sa.String(length=50), nullable=True),
    sa.Column('alloted_products', sa.String(length=255), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('sales_representative_id', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['sales_representative_id'], ['User.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('CustomerBillingAddress',
    sa.Column('suite_apartment', sa.String(length=255), nullable=True),
    sa.Column('address_line_1', sa.String(length=255), nullable=False),
    sa.Column('address_line_2', sa.String(length=255), nullable=True),
    sa.Column('city', sa.String(length=255), nullable=False),
    sa.Column('state', sa.String(length=255), nullable=False),
    sa.Column('country', sa.String(length=255), nullable=False),
    sa.Column('zip_code', sa.Integer(), nullable=True),
    sa.Column('latitude', sa.Float(), nullable=True),
    sa.Column('longitude', sa.Float(), nullable=True),
    sa.Column('is_default', sa.Boolean(), nullable=True),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['Customer.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('CustomerDocuments',
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('attachment', sa.String(length=500), nullable=True),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['Customer.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('CustomerShippingAddress',
    sa.Column('address_line_1', sa.String(length=255), nullable=False),
    sa.Column('address_line_2', sa.String(length=255), nullable=True),
    sa.Column('suite_apartment', sa.String(length=255), nullable=True),
    sa.Column('city', sa.String(length=255), nullable=False),
    sa.Column('state', sa.String(length=255), nullable=False),
    sa.Column('country', sa.String(length=255), nullable=False),
    sa.Column('zip_code', sa.Integer(), nullable=True),
    sa.Column('latitude', sa.Float(), nullable=True),
    sa.Column('longitude', sa.Float(), nullable=True),
    sa.Column('is_default', sa.Boolean(), nullable=True),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['Customer.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('MultipleCustomerPerson',
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('phone', sa.String(length=20), nullable=True),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['Customer.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('MultipleCustomerPerson')
    op.drop_table('CustomerShippingAddress')
    op.drop_table('CustomerDocuments')
    op.drop_table('CustomerBillingAddress')
    op.drop_table('Customer')
    # ### end Alembic commands ###
