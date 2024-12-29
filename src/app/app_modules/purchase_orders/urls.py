from flask import Blueprint
from .views import ProductListView,PurchaseOrderDataTableView,PurchaseOrderCreateView

po_bp = Blueprint('po_bp', __name__)

po_bp.add_url_rule('/purchase-orders', view_func=ProductListView.as_view('purchase_order'))
po_bp.add_url_rule('/api/purchase-order', view_func=PurchaseOrderDataTableView.as_view('purchase_order_data_table'))
po_bp.add_url_rule("/purchase-orders/create/",view_func=PurchaseOrderCreateView.as_view('create_purchase_order')),