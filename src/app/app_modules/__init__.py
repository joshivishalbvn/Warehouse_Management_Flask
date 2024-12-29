from .dashboard.urls import dashboard_bp
from .company.urls import company_bp
from .users.urls import user_bp
from .warehouse.urls import wh_bp
from .zones.urls import zone_bp
from .products.urls import product_bp
from .vendors.urls import vendor_bp
from .stocks.urls import stock_bp
from .customers.urls import customer_bp
from .purchase_orders.urls import po_bp

blue_prints = [dashboard_bp,user_bp,company_bp,wh_bp,zone_bp,product_bp,vendor_bp,stock_bp,customer_bp,po_bp]