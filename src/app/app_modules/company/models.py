import os

from flask import url_for
from app import db
from app.app_modules.base.models import BaseModel


class Company(BaseModel):

    __tablename__ = 'company'

    ACTIVE = "Active"
    INACTIVE = "Inactive"

    STATUS_CHOICES = (
        (ACTIVE, ACTIVE),
        (INACTIVE, INACTIVE),
    )
    
    name    = db.Column(db.String(100), nullable=False)
    email   = db.Column(db.String(120), unique=True, nullable=False)
    phone   = db.Column(db.String(20), nullable=True)
    logo    = db.Column(db.String(255), nullable=True)  
    status  = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return self.name
    
    @property
    def get_warehouse_count(self):
        return len(self.warehouses)
    
    @property
    def get_zones_count(self):
        from ..zones.models import Zone
        from ..warehouse.models import Warehouse
        return Zone.query.join(Warehouse).filter_by(company_id=self.id).count()
    
    @property
    def get_employees_count(self):
        # from app_modules.users.models import User
        # return User.query.filter_by(company_id=self.id).count()
        return 0
    
    @property
    def get_products_count(self):
        # from app_modules.products.models import Product
        # return Product.query.filter_by(company_id=self.id).count()
        return 0
    
    def set_logo(self, file):
        COMPANY_LOGO_PATH = "static/uploads/company_logos/"
        from werkzeug.utils import secure_filename
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(COMPANY_LOGO_PATH, filename)
            file.save(file_path)
            self.logo =  file_path
        else:
            raise ValueError("No file provided.")
        
    @property
    def update_url(self):
        return url_for('company_bp.update_company', id=self.id)

    
class ContactPerson(BaseModel):

    __tablename__ = 'contact_person'
    
    name        = db.Column(db.String(100), nullable=False)
    email       = db.Column(db.String(120), unique=True, nullable=False)
    phone       = db.Column(db.String(20), nullable=True)
    company_id  = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=True)
    company     = db.relationship('Company', backref=db.backref('users', lazy=True))


    def __repr__(self):
        return f'<ContactPerson {self.name}>'