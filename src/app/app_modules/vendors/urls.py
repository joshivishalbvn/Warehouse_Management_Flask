from flask import Blueprint
from .views import CreateVendorView, VendorUpdateView, DeleteVendor, VendorDataTableView , VendorListView , VendorDetailsView,VendorPurchaseOrderDatatableList,GetVendors

vendor_bp = Blueprint('vendor_bp', __name__)

vendor_bp.add_url_rule('/vendors', view_func=VendorListView.as_view('vendor_list'))
vendor_bp.add_url_rule('/add-vendor', view_func=CreateVendorView.as_view('create_vendor'))
vendor_bp.add_url_rule('/<int:id>/update-vendor', view_func=VendorUpdateView.as_view('update_vendor'))
vendor_bp.add_url_rule('/<int:id>/details-vendor', view_func=VendorDetailsView.as_view('vendor_details'))
vendor_bp.add_url_rule('/<int:id>/delete-vendor/', view_func=DeleteVendor.as_view('delete_vendor'))
vendor_bp.add_url_rule('/ajax/get-vendor/', view_func=GetVendors.as_view('get_vendor_ajax'))

# <------------ Datatable ------------>
vendor_bp.add_url_rule('/api/vendor', view_func=VendorDataTableView.as_view('vendor_data_table'))
vendor_bp.add_url_rule("/api/purchase-history/",view_func=VendorPurchaseOrderDatatableList.as_view('purchase_history_ajax'))
# <------------ Datatable ------------>

