from flask import url_for
from app import db
from app.app_modules.base.models import BaseModel


class User(BaseModel):

    """
    User Detail Model
    """
    
    __tablename__ = 'User'

    ACTIVE   = "active"
    INACTIVE = "inactive"
    
    STATUS_CHOICES = (
        (ACTIVE, ACTIVE),
        (INACTIVE, INACTIVE),
    )
    
    SUPER_ADMIN          = "Super Admin"
    COMPANY_ADMIN        = "Company Admin"
    SALES_REPRESENTATIVE = "Sales Representative"
    WAREHOUSE_MANAGER    = "Warehouse Manager"
    CUSTOMER             = "Customer"

    
    USER_ROLE = (
        (SUPER_ADMIN, SUPER_ADMIN),
        (COMPANY_ADMIN, COMPANY_ADMIN),
        (SALES_REPRESENTATIVE, SALES_REPRESENTATIVE),
        (WAREHOUSE_MANAGER, WAREHOUSE_MANAGER),
        (CUSTOMER, CUSTOMER),
    )
    
    first_name  = db.Column(db.String(50), nullable=True)
    last_name   = db.Column(db.String(50), nullable=True)
    email       = db.Column(db.String(255), nullable=False)
    image       = db.Column(db.String(255), nullable=True) 
    mobile      = db.Column(db.String(15), nullable=True)
    role        = db.Column(db.String(100), nullable=True)
    password    = db.Column(db.String(512))
    is_superuser= db.Column(db.Boolean, default=False)
    company_id  = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=True)
    company     = db.relationship('Company', backref=db.backref('company_users', lazy=True))

    def __repr__(self):
        return f'<User {self.email}>'
    
    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    # @property
    # def get_company_id(self):
    #     return self.company_id if self.company else None
    
    def set_password(self, password):
        from werkzeug.security import generate_password_hash
        self.password = generate_password_hash(password)

    def delete_url(self):
        """Returns the URL to delete this user."""
        return url_for('user_bp.delete_user', user_id=self.id)
    
    @property
    def update_url(self):
        """Returns the URL to delete this user."""
        return url_for('user_bp.update_user', id=self.id)
    
class SalesRepManager:
    def __init__(self, session):
        self.session = session

    def query(self):
        return self.session.query(User).filter_by(role=User.SALES_REPRESENTATIVE)

class SalesRep(User):
    __mapper_args__ = {
        'polymorphic_identity': User.SALES_REPRESENTATIVE,
        'concrete': True
    }

    @property
    def is_sales_rep(self):
        return True