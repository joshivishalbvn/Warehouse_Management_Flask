from app import db
from sqlalchemy.sql import func
from ..base.models import BaseModel
from ..company.models import Company
from ..products.models import Product , ProductCase
from ..vendors.models import Vendor
from ..warehouse.models import Warehouse
from ..zones.models import Zone
from ..users.models import User

class Stock(BaseModel):

    __tablename__ = 'stock'

    total_stock     = db.Column(db.Integer, default=0)

    company_id      = db.Column(db.Integer, db.ForeignKey(Company.id), nullable=True)
    company         = db.relationship(Company, backref=db.backref('company_stock', lazy=True))
    vendor_id       = db.Column(db.Integer, db.ForeignKey(Vendor.id), nullable=True)
    vendor          = db.relationship(Vendor, backref=db.backref('vendor', lazy=True))
    warehouse_id    = db.Column(db.Integer, db.ForeignKey(Warehouse.id), nullable=True)
    warehouse       = db.relationship(Warehouse, backref=db.backref('stock_warehouse', lazy=True))
    product_id      = db.Column(db.Integer, db.ForeignKey(Product.id), nullable=False)
    product         = db.relationship(Product, backref=db.backref('products', lazy=True))

    @property
    def get_locked_stock(self):
        total_locked_stock = db.session.query(func.sum(StockHistory.locked_quantity)).filter_by(product_id=self.product_id).scalar()
        return total_locked_stock or 0
    
    @property
    def get_load_stock(self):
        total_load_stock = db.session.query(func.sum(StockHistory.load_quantity)).filter_by(product_id=self.product_id).scalar()
        return total_load_stock or 0

    def __repr__(self):
        return f'<Stock {self.product.name}>'

class StockHistory(BaseModel):

    __tablename__ = 'stock_history'

    IN = "in"
    OUT = "out"

    TYPE_CHOICES = [
        (IN, 'In'),
        (OUT, 'Out'),
    ]

    CREATED = "created"
    UPDATED = "updated"

    STATUS_CHOICES = [
        (CREATED, CREATED),
        (UPDATED, UPDATED),
    ]

    no_of_case              = db.Column(db.Integer, default=0)
    manufacture_date        = db.Column(db.Date, nullable=True)
    expiry_date             = db.Column(db.Date, nullable=True)
    stock                   = db.Column(db.Integer, default=0)
    affected_stock          = db.Column(db.Integer, default=0)
    before_stock            = db.Column(db.Integer, default=0)
    per_piece_price         = db.Column(db.Integer, default=0)
    total_amount            = db.Column(db.Numeric(10, 2), default=0)
    type                    = db.Column(db.String(50), default=IN)
    locked_quantity         = db.Column(db.Integer, default=0, nullable=True)
    load_quantity           = db.Column(db.Integer, default=0, nullable=True)
    remark                  = db.Column(db.Text, nullable=True)
    status                  = db.Column(db.String(100), default=CREATED)
    is_deleted              = db.Column(db.Boolean, default=False)
    removed_at              = db.Column(db.Date, nullable=True)

    product_id              = db.Column(db.Integer, db.ForeignKey(Product.id), nullable=False)
    product                 = db.relationship(Product, backref=db.backref('product_stock', lazy=True))
    product_case_id         = db.Column(db.Integer, db.ForeignKey(ProductCase.id), nullable=True)
    product_case            = db.relationship(ProductCase, backref=db.backref('product_stock_set', lazy=True))
    modified_by_id          = db.Column(db.Integer, db.ForeignKey(User.id), nullable=True)
    modified_by             = db.relationship(User, backref=db.backref('stock_set', lazy=True))
    warehouse_id            = db.Column(db.Integer, db.ForeignKey(Warehouse.id), nullable=True)
    warehouse               = db.relationship(Warehouse, backref=db.backref('warehouse_stock_history', lazy=True))
    zone_id                 = db.Column(db.Integer, db.ForeignKey(Zone.id), nullable=False)
    zone                    = db.relationship(Zone, backref=db.backref('zone_stock_history', lazy=True))
    vendor_id               = db.Column(db.Integer, db.ForeignKey(Vendor.id), nullable=True)
    vendor                  = db.relationship(Vendor, backref=db.backref('stock_set', lazy=True))

    @property
    def get_zone_wise_current_stock(self):
        stock_agg = db.session.query(
            func.sum(StockHistory.affected_stock).label('total_affected_stock'),
            func.sum(StockHistory.locked_quantity).label('total_locked_quantity'),
            func.sum(StockHistory.load_quantity).label('total_load_quantity')
        ).filter(
            StockHistory.zone_id == self.zone_id,
            StockHistory.product_id == self.product_id,
            StockHistory.status == StockHistory.CREATED,
            StockHistory.affected_stock > StockHistory.locked_quantity,
            StockHistory.is_deleted == False
        ).one_or_none()

        total_affected_stock = stock_agg.total_affected_stock or 0
        total_locked_quantity = stock_agg.total_locked_quantity or 0
        total_load_quantity = stock_agg.total_load_quantity or 0

        return total_affected_stock - (total_locked_quantity + total_load_quantity) if total_affected_stock >= (total_locked_quantity + total_load_quantity) else 0

    def __repr__(self):
        return f'<StockHistory {self.product.name}>'

# class ManageStockHistory(BaseModel):

#     __tablename__ = 'manage_stock_history'

#     IN = "in"
#     OUT = "out"

#     TYPE_CHOICES = [
#         (IN, 'In'),
#         (OUT, 'Out'),
#     ]

#     affected_stock  = db.Column(db.Integer, default=0)
#     current_stock   = db.Column(db.Integer, default=0)
#     per_piece_price = db.Column(db.Integer, default=0)
#     total_amount    = db.Column(db.Numeric(10, 2), default=0)
#     stock_type      = db.Column(db.String(50), default=IN)

#     stock_id        = db.Column(db.Integer, db.ForeignKey(StockHistory.id), nullable=True)
#     stock           = db.relationship(StockHistory, backref=db.backref('manage_stock_history_set', lazy=True))
#     load_product_id = db.Column(db.Integer, db.ForeignKey('load_order_products.id'), nullable=True)
#     load_product    = db.relationship('LoadOrderProducts', backref=db.backref('manage_stock_history_set', lazy=True))
#     product_id      = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
#     product         = db.relationship('Product', backref=db.backref('product_manage_stock_history', lazy=True))
#     product_case_id = db.Column(db.Integer, db.ForeignKey('product_case.id'), nullable=True)
#     product_case    = db.relationship('ProductCase', backref=db.backref('product_manage_stock_history', lazy=True))
#     modified_by_id  = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
#     modified_by     = db.relationship('User', backref=db.backref('manage_stock_history_set', lazy=True))
#     warehouse_id    = db.Column(db.Integer, db.ForeignKey('warehouse.id'), nullable=True)
#     warehouse       = db.relationship('Warehouse', backref=db.backref('warehouse_manage_stock_history', lazy=True))
#     zone_id         = db.Column(db.Integer, db.ForeignKey('zone.id'), nullable=False)
#     zone            = db.relationship('Zone', backref=db.backref('zone_manage_stock_history', lazy=True))
#     vendor_id       = db.Column(db.Integer, db.ForeignKey('vendor.id'), nullable=True)
#     vendor          = db.relationship('Vendor', backref=db.backref('manage_stock_history', lazy=True))

#     def __repr__(self):
#         return f'<ManageStockHistory {self.product.name}>'

# class LockedProductStock(BaseModel):

#     __tablename__ = 'locked_product_stock'

#     locked_quantity  = db.Column(db.Integer, default=0, nullable=True)
#     is_deleted       = db.Column(db.Boolean, default=False)

#     order_id         = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
#     order            = db.relationship('Order', backref=db.backref('locked_product_stock_set', lazy=True))
#     order_product_id = db.Column(db.Integer, db.ForeignKey('order_product.id'), nullable=False)
#     order_product    = db.relationship('OrderProduct', backref=db.backref('locked_product_stock_set', lazy=True))
#     stock_id         = db.Column(db.Integer, db.ForeignKey('stock_history.id'), nullable=False)
#     stock            = db.relationship('StockHistory', backref=db.backref('locked_product_stock_set', lazy=True))

# class MissingProductStock(BaseModel):

#     __tablename__ = 'missing_product_stock'

#     missing_quantity = db.Column(db.Integer, default=0, nullable=True)
#     order_id         = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
#     order            = db.relationship('Order', backref=db.backref('missing_product_stock_set', lazy=True))
#     order_product_id = db.Column(db.Integer, db.ForeignKey('order_product.id'), nullable=False)
#     order_product    = db.relationship('OrderProduct', backref=db.backref('missing_product_stock_set', lazy=True))

#     def __repr__(self):
#         return f'<MissingProductStock {self.order_product}>'
