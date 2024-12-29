import os
from app import db
from ..vendors.models import Vendor
from ..company.models import Company
from ..base.models import BaseModel
from ..products.models import Product,ProductCase

class PurchaseOrder(BaseModel):

    __tablename__ = 'PurchaseOrder'
    
    CREATED = "created"
    UNLOADING = "unloading"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

    STATUS_CHOICES = (
        (CREATED, CREATED),
        (UNLOADING, UNLOADING),
        (COMPLETED, COMPLETED),
        (CANCELLED, CANCELLED),
    )

    INVOICE_PATH =  os.path.join('app', 'static', 'uploads', 'purchase_order_invoices')
    
    purchase_id  = db.Column(db.String(20), nullable=True)
    status       = db.Column(db.String(100), default=CREATED)
    total_price  = db.Column(db.Numeric(10, 2), default=0.0)
    invoice      = db.Column(db.String, nullable=True)  
    remarks      = db.Column(db.Text, nullable=True)
    vendor_id    = db.Column(db.Integer, db.ForeignKey(Vendor.id), nullable=True)
    vendor       = db.relationship(Vendor, backref='purchase_orders', lazy=True)
    company_id   = db.Column(db.Integer, db.ForeignKey(Company.id), nullable=True)
    company      = db.relationship(Company, backref='purchase_orders', lazy=True)

    @property
    def get_invoice_name(self):
        return self.invoice.split('/')[-1]

    @property
    def get_total(self):
        return int(self.total_price)

    def __repr__(self):
        return f'<PurchaseOrder {self.id}>'

class PurchaseOrderProducts(BaseModel):

    __tablename__ = 'PurchaseOrderProducts'
    
    UNDELIVERED = "undelivered"
    UNLOADED = "unloaded"

    STATUS_CHOICES = (
        (UNDELIVERED, UNDELIVERED),
        (UNLOADED, UNLOADED),
    )
    
    case_quantity       = db.Column(db.Integer, nullable=False)
    total_pieces        = db.Column(db.Integer, default=0)
    batch_number        = db.Column(db.String(100), nullable=True)
    per_piece_price     = db.Column(db.Integer, default=0)
    status              = db.Column(db.String(50), default=UNDELIVERED)
    amount              = db.Column(db.Integer, default=0)
    
    purchase_order_id   = db.Column(db.Integer, db.ForeignKey(PurchaseOrder.id), nullable=True)
    purchase_order      = db.relationship(PurchaseOrder, backref='purchase_order_products', lazy=True)
    product_id          = db.Column(db.Integer, db.ForeignKey(Product.id), nullable=True)
    product             = db.relationship(Product, backref='purchase_order_products', lazy=True)
    case_size_id        = db.Column(db.Integer, db.ForeignKey(ProductCase.id), nullable=True)
    case_size           = db.relationship(ProductCase, backref='purchase_order_products', lazy=True)

    def get_unloaded_piece(self):
        unloaded_products = PurchaseOrderProductUnloadHistory.query.filter_by(purchase_order_product_id=self.id).all()
        unloaded_stock = sum([up.unload_stock for up in unloaded_products]) if unloaded_products else 0
        return unloaded_stock

    def get_undelivered_piece(self):
        unloaded_products = PurchaseOrderProductUnloadHistory.query.filter_by(purchase_order_product_id=self.id).all()
        unloaded_stock = sum([up.unload_stock for up in unloaded_products]) if unloaded_products else 0
        return max(0, self.total_pieces - unloaded_stock)

    @property
    def get_total_qty(self):
        return self.case_quantity * self.case_size.quantity

    def __repr__(self):
        return f'<PurchaseOrderProducts {self.product.name}>'

class PurchaseOrderProductUnloadHistory(BaseModel):

    __tablename__ = 'PurchaseOrderProductUnloadHistory'
    
    unload_stock              = db.Column(db.Integer, default=0)
    purchase_order_product_id = db.Column(db.Integer, db.ForeignKey(PurchaseOrderProducts.id), nullable=True)
    purchase_order_product    = db.relationship(PurchaseOrderProducts, backref='unload_history', lazy=True)

    def __repr__(self):
        return f'<PurchaseOrderProductUnloadHistory {self.id}>'

class VendorPayments(BaseModel):

    __tablename__ = 'VendorPayments'
    
    paid_amount         = db.Column(db.Float, default=0.0)
    due_amount          = db.Column(db.Float, default=0.0)

    purchase_order_id   = db.Column(db.Integer, db.ForeignKey(PurchaseOrder.id), nullable=True)
    purchase_order      = db.relationship(PurchaseOrder, backref='vendor_payments', lazy=True)
    vendor_id           = db.Column(db.Integer, db.ForeignKey(Vendor.id), nullable=True)
    vendor              = db.relationship(Vendor, backref='vendor_payments', lazy=True)

    def __repr__(self):
        return f'<VendorPayments {self.id}>'
