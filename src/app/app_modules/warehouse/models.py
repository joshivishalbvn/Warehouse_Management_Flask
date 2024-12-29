from app import db
from app.app_modules.base.models import BaseModel


class Warehouse(BaseModel):

    __tablename__ = 'Warehouse'

    ACTIVE = "active"
    INACTIVE = "inactive"
    
    STATUS_CHOICES = (
        (ACTIVE, ACTIVE),
        (INACTIVE, INACTIVE),
    )

    name            = db.Column(db.String(100), nullable=False)
    address_line_1  = db.Column(db.String(150), nullable=True)
    address_line_2  = db.Column(db.String(150), nullable=True)
    city            = db.Column(db.String(50), nullable=True)
    state           = db.Column(db.String(50), nullable=True)
    zip_code        = db.Column(db.Integer, nullable=True)
    country         = db.Column(db.String(50), nullable=True)
    status          = db.Column(db.String(100), nullable=True)
    company_id      = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=True)
    company         = db.relationship('Company', backref=db.backref('warehouses', lazy=True))
    manager_id      = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=True)
    manager         = db.relationship('User', backref=db.backref('warehouse_manager', lazy=True))
    
    @property
    def zone_count(self):
        return len(self.warehouse_zone)

    @property
    def product_count(self):
        # from app_modules.manage_stock.models import StockHistory
        # stock_list = db.session.query(StockHistory).filter(
        #     StockHistory.warehouse_id == self.id,
        #     StockHistory.status == 'Created',
        #     StockHistory.is_deleted == False
        # ).distinct(StockHistory.product_id).count()
        # return stock_list
        return 0
    
    @property
    def get_stock_count(self):
        # from app_modules.manage_stock.models import StockHistory
        # stock_list = db.session.query(StockHistory).filter(
        #     StockHistory.warehouse_id == self.id,
        #     StockHistory.status == 'Created',
        #     StockHistory.is_deleted == False
        # ).all()

        # if stock_list:
        #     total_affected = sum(stock.affected_stock for stock in stock_list)
        #     total_locked = sum(stock.locked_quantity for stock in stock_list)
        #     total_load = sum(stock.load_quantity for stock in stock_list)
        #     available_stock = total_affected - (total_locked + total_load)
        #     return available_stock
        # else:
        #     return 0

        return 0

    def __repr__(self):
        return f'<Warehouse {self.name}>'