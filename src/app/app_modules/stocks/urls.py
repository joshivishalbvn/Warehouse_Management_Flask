from flask import Blueprint
from .views import CreateStockView , StockDataTableView

stock_bp = Blueprint('stock_bp', __name__)

stock_bp.add_url_rule('/create-stock', view_func=CreateStockView.as_view('create_stock'))
stock_bp.add_url_rule('/api/stocks', view_func=StockDataTableView.as_view('stock_data_table'))