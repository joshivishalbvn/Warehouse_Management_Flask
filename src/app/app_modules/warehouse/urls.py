from flask import Blueprint

from .views import WareHouseList, CreateWarehouse, UpdateWarehouse , WarehouseDetails , Loadmanager,WarehouseDataTableView

wh_bp = Blueprint('wh_bp', __name__)

wh_bp.add_url_rule('/warehouses', view_func=WareHouseList.as_view('warehouse_list'))
wh_bp.add_url_rule('/create-warehouse', view_func=CreateWarehouse.as_view('create_warehouse'))
wh_bp.add_url_rule('/<int:id>/update-warehouse', view_func=UpdateWarehouse.as_view('update_warehouse'))
wh_bp.add_url_rule('/<int:id>/warehouse-details', view_func=WarehouseDetails.as_view('warehouse_details'))
wh_bp.add_url_rule('/load_manager', view_func=Loadmanager.as_view('load_manager'))
wh_bp.add_url_rule('/api/warehouses', view_func=WarehouseDataTableView.as_view('warehouse_data_table'))
