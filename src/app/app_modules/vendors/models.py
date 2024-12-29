import os
from app import db
from ..base.models import BaseModel



class Vendor(BaseModel):

    __tablename__ = 'Vendor'

    ACTIVE = "Active"
    INACTIVE = "Inactive"

    VENDOR_STATUS = [
        (ACTIVE, ACTIVE),
        (INACTIVE, INACTIVE),
    ]

    full_name       = db.Column(db.String(50), nullable=True)
    address_line_1  = db.Column(db.String(100), nullable=True)
    address_line_2  = db.Column(db.String(100), nullable=True)
    state           = db.Column(db.String(50), nullable=False)
    city            = db.Column(db.String(50), nullable=False)
    zip_code        = db.Column(db.Integer, nullable=True)
    country         = db.Column(db.String(50), nullable=True)
    email           = db.Column(db.String(255), nullable=False)
    phone           = db.Column(db.String(20), nullable=True)
    website         = db.Column(db.String(200), nullable=True)
    status          = db.Column(db.String(100), nullable=True)

    company_id      = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=True)
    company         = db.relationship('Company', backref=db.backref('vendors', lazy=True))

    def __repr__(self):
        return f'<Vendor {self.full_name}>'
    
    @property
    def get_status_display(self):
        return dict(self.VENDOR_STATUS).get(self.status, '')

class MultipleVendorDocument(BaseModel):
    
    __tablename__ = 'multiple_vendor_document'

    name      = db.Column(db.String(255), nullable=True)
    documents = db.Column(db.String(255), nullable=True)  

    vendor_id = db.Column(db.Integer, db.ForeignKey('Vendor.id'), nullable=False)
    vendor    = db.relationship('Vendor', backref=db.backref('vendor_details', lazy=True))

    @property
    def get_file_name(self):
        return os.path.basename(self.documents) if self.documents else ''

    def __repr__(self):
        return f'<MultipleVendorDocument {self.name}>'