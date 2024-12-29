import os
from app import db
from ..users.models import User
from app.app_modules.base.models import BaseModel

class Customer(BaseModel):

    __tablename__ = 'Customer'

    ALLOTED_PRODUCTS_FILE_PATH = os.path.join('app', 'static', 'uploads', 'customer_alloted_products')

    DISTRIBUTOR = "Distributor"
    WHOLESALE = "Wholesale"
    RETAIL = "Retail"

    CUSTOMER_CHOICES = (
        (DISTRIBUTOR, DISTRIBUTOR),
        (WHOLESALE, WHOLESALE),
        (RETAIL, RETAIL),
    )

    ACTIVE = "Active"
    INACTIVE = "Inactive"

    STATUS_CHOICES = (
        (ACTIVE, ACTIVE),
        (INACTIVE, INACTIVE),
    )

    status                  = db.Column(db.String(20), default=ACTIVE)
    type                    = db.Column(db.String(50), default=RETAIL)
    bill_to                 = db.Column(db.String(50), nullable=True)
    ship_to                 = db.Column(db.String(50), nullable=True)
    alloted_products        = db.Column(db.String(255), nullable=True)  
    user_id                 = db.Column(db.Integer, db.ForeignKey(User.id), nullable=True)
    user                    = db.relationship(User,foreign_keys=[user_id], backref='customers')
    sales_representative_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=True)
    sales_representative    = db.relationship(User, foreign_keys=[sales_representative_id], backref='sales_rep_customers')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    @property
    def get_customer_phone_number(self):
        # customer_phone = MultipleCustomerPerson.query.filter_by(customer_id=self.id).first()
        # return customer_phone.phone if customer_phone else None
        return 0

    @property
    def get_last_order_date(self):
        # last_order = Order.query.filter_by(customer_id=self.id).order_by(Order.created_at.desc()).first()
        # return last_order.created_at if last_order else None
        return 0

class MultipleCustomerPerson(BaseModel):

    __tablename__ = 'MultipleCustomerPerson'

    name        = db.Column(db.String(255), nullable=False)
    email       = db.Column(db.String(255), nullable=False)
    phone       = db.Column(db.String(20), nullable=True)
    customer_id = db.Column(db.Integer, db.ForeignKey(Customer.id), nullable=False)
    customer    = db.relationship(Customer, backref='customer_details')

class CustomerShippingAddress(BaseModel):

    __tablename__ = 'CustomerShippingAddress'

    address_line_1  = db.Column(db.String(255), nullable=False)
    address_line_2  = db.Column(db.String(255), nullable=True)
    suite_apartment = db.Column(db.String(255), nullable=True)
    city            = db.Column(db.String(255), nullable=False)
    state           = db.Column(db.String(255), nullable=False)
    country         = db.Column(db.String(255), nullable=False)
    zip_code        = db.Column(db.Integer, nullable=True)
    latitude        = db.Column(db.Float, nullable=True)
    longitude       = db.Column(db.Float, nullable=True)
    is_default      = db.Column(db.Boolean, default=False)
    customer_id     = db.Column(db.Integer, db.ForeignKey(Customer.id), nullable=False)
    customer        = db.relationship(Customer, backref='customer_shipping_address')

class CustomerBillingAddress(BaseModel):

    __tablename__ = 'CustomerBillingAddress'

    suite_apartment = db.Column(db.String(255), nullable=True)
    address_line_1  = db.Column(db.String(255), nullable=False)
    address_line_2  = db.Column(db.String(255), nullable=True)
    city            = db.Column(db.String(255), nullable=False)
    state           = db.Column(db.String(255), nullable=False)
    country         = db.Column(db.String(255), nullable=False)
    zip_code        = db.Column(db.Integer, nullable=True)
    latitude        = db.Column(db.Float, nullable=True)
    longitude       = db.Column(db.Float, nullable=True)
    is_default      = db.Column(db.Boolean, default=False)
    customer_id     = db.Column(db.Integer, db.ForeignKey(Customer.id), nullable=False)
    customer        = db.relationship(Customer, backref='customer_billing_address')

class CustomerDocuments(BaseModel):

    __tablename__ = 'CustomerDocuments'

    DOCUMENTS_FILE_PATH = os.path.join('app', 'static', 'uploads', 'customer_documents')
    DOCUMENTS_FILE_ROOT_PATH = os.path.join('uploads','customer_documents')

    name        = db.Column(db.String(255), nullable=False)
    attachment  = db.Column(db.String(500), nullable=True)  
    customer_id = db.Column(db.Integer, db.ForeignKey(Customer.id), nullable=False)
    customer    = db.relationship(Customer, backref='customer_documents')

# class CustomerCredits(BaseModel):

#     __tablename__ = 'CustomerCredits'

#     CHECK = "check"
#     CASH = "cash"
#     CREDIT_CARD = "credit card"
#     MONEY_ORDER = "money order"
#     ELECTRONIC_TRANSFER = "electronic transfer"

#     PAYMENT_MODE_CHOICE = (
#         (CHECK,'Check'),
#         (CASH,'Cash'),
#         (CREDIT_CARD,'Credit Card'),
#         (MONEY_ORDER,'Money Order'),
#         (ELECTRONIC_TRANSFER,'Electronic Transfer')
#     )

#     receive_date = db.Column(db.Date, default=datetime.date.today)
#     entry_date = db.Column(db.Date, default=datetime.date.today)
#     amount = db.Column(db.Float, default=0.0)
#     payment_mode = db.Column(db.String(30), default=CASH)
#     reference_id = db.Column(db.Integer, nullable=True)
#     remark = db.Column(db.String(20), nullable=True)

#     customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
#     customer = db.relationship('Customer', backref='customer_credits')
#     load_order_id = db.Column(db.Integer, db.ForeignKey('load_order.id'), nullable=True)
#     load_order = db.relationship('LoadOrder', backref='load_order_credits')

# class CustomerCreditsHistory(BaseModel):
#     CREDITED = "credited"
#     DEBITED = "debited"

#     ACTION_CHOICES = [CREDITED, DEBITED]

#     customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
#     load_order_id = db.Column(db.Integer, db.ForeignKey('load_order.id'), nullable=True)
#     amount = db.Column(db.Float, default=0.0)
#     action = db.Column(db.String(30), nullable=True)
#     is_credited = db.Column(db.Boolean, default=False)

#     customer = db.relationship('Customer', backref='customer_credits_history')
#     load_order = db.relationship('LoadOrder', backref='load_order_credits_history')