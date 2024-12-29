from flask import Blueprint
from .views import ProductCaseDeleteView, ProductCaseUpdateView, ProductCreateFromCSVFormView, ProductDetailsView, ProductListView , CreateProduct , ProductDataTableView , DeleteProduct , ProductUpdateView , ProductDetailView , ProductBarcodeList , CreateProductBarcode , CreateProductCase,ProductCasesDataTableView , ProductBarcodeDataTableView , ProductBarcodeDeleteView,ProductBarcodeUpdateView,GetProductsAjax , GetQuantityByCaseAjax

product_bp = Blueprint('product_bp', __name__)

product_bp.add_url_rule('/products', view_func=ProductListView.as_view('product_list'))
product_bp.add_url_rule('/create-product', view_func=CreateProduct.as_view('create_product'))
product_bp.add_url_rule('/<int:id>/update-product', view_func=ProductUpdateView.as_view('update_product'))
product_bp.add_url_rule('/product/<int:id>/delete/', view_func=DeleteProduct.as_view('delete_product'))
product_bp.add_url_rule('/<int:id>/details', view_func=ProductDetailView.as_view('product_details'))
product_bp.add_url_rule('/api/products', view_func=ProductDataTableView.as_view('product_data_table'))
product_bp.add_url_rule('/api/get-products', view_func=GetProductsAjax.as_view('get_products_ajax'))
product_bp.add_url_rule('/api/get-products-details', view_func=ProductDetailsView.as_view('get_product_details_ajax'))

product_bp.add_url_rule("/product-create-from-csv/", view_func=ProductCreateFromCSVFormView.as_view("product_create_from_csv")),


product_bp.add_url_rule('/create-case', view_func=CreateProductCase.as_view('create_product_case'))
product_bp.add_url_rule('/<int:id>/update-case', view_func=ProductCaseUpdateView.as_view('update_product_case'))
product_bp.add_url_rule('/<int:id>/delete-case', view_func=ProductCaseDeleteView.as_view('delete_product_case'))
product_bp.add_url_rule('/api/products-case', view_func=ProductCasesDataTableView.as_view('product_case_data_table'))
product_bp.add_url_rule('/api/get-quantity', view_func=GetQuantityByCaseAjax.as_view('get_quantity_ajax'))


product_bp.add_url_rule('/barcode', view_func=CreateProductBarcode.as_view('create_barcode'))
product_bp.add_url_rule('/<int:id>/update-barcode', view_func=ProductBarcodeUpdateView.as_view('update_product_barcode'))
product_bp.add_url_rule('/<int:id>/delete-barcode', view_func=ProductBarcodeDeleteView.as_view('delete_product_barcode'))
product_bp.add_url_rule('/api/products-bacode', view_func=ProductBarcodeDataTableView.as_view('product_barcode_data_table'))
product_bp.add_url_rule('/<int:id>/barcodes', view_func=ProductBarcodeList.as_view('product_barcode_list'))