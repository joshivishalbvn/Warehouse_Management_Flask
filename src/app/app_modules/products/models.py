from app import db
from app.app_modules.base.models import BaseModel

class Product(BaseModel):
    __tablename__ = 'Products'

    ACTIVE = 'Active'
    INACTIVE = 'Inactive'

    STATUS_CHOICES = (
        (ACTIVE, ACTIVE),
        (INACTIVE, INACTIVE),
    )

    name                = db.Column(db.String(50), nullable=False)
    code                = db.Column(db.String(50), unique=True, nullable=True)
    status              = db.Column(db.String(100), default=ACTIVE)
    total_quantity_sold = db.Column(db.Integer, default=0)
    company_id          = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=True)
    company             = db.relationship('Company', backref=db.backref('products', lazy=True))

    images              = db.relationship('ProductImage', back_populates='product',cascade='all, delete-orphan')
    cases               = db.relationship('ProductCase', back_populates='product', cascade='all, delete-orphan')
    barcodes            = db.relationship('Barcode', back_populates='product',cascade='all, delete-orphan')

    @property
    def get_product_image(self):
        return self.images[0].image_url if self.images else ""

    @property
    def get_total_available_stock(self):
        return sum(case.get_total_stock for case in self.cases)

    def __str__(self):
        return self.name

class ProductImage(BaseModel):
    __tablename__ = 'ProductImage'

    image_url  = db.Column(db.String, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('Products.id', ondelete='CASCADE'), nullable=False)

    product = db.relationship('Product', back_populates='images')

class ProductCase(BaseModel):
    __tablename__ = 'ProductCase'

    weight             = db.Column(db.Float, default=0)
    quantity           = db.Column(db.Integer, default=0)
    cubic_meter_volume = db.Column(db.Float, default=0)
    product_id         = db.Column(db.Integer, db.ForeignKey('Products.id'), nullable=False)
    product            = db.relationship('Product', back_populates='cases')

    @property
    def get_total_stock(self):
        return 0

    def __str__(self):
        return f"{self.quantity} Qty, {self.weight} Oz, {self.cubic_meter_volume} CMV"

class Barcode(BaseModel):
    __tablename__ = 'Barcode'

    number = db.Column(db.String(255), unique=True, nullable=False)
    code_url = db.Column(db.String(255)) 
    product_id = db.Column(db.Integer, db.ForeignKey('Products.id'), nullable=False)
    product = db.relationship('Product', back_populates='barcodes')

class CSVFile(BaseModel):
    __tablename__ = 'CSVFile'

    csv_file_url = db.Column(db.String, nullable=False)

