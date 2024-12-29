from flask import Blueprint
from .views import *

customer_bp = Blueprint('customer_bp', __name__)

customer_bp.add_url_rule('/customers', view_func=CustomerListView.as_view('customer_list'))
customer_bp.add_url_rule('/customer/<int:id>/delete/', view_func=DeleteCustomer.as_view('delete_customer'))
customer_bp.add_url_rule('/create-customer', view_func=CreateCustomerView.as_view('create_customer'))
customer_bp.add_url_rule('/customer/<int:id>/update/', view_func=CustomerUpdateView.as_view('update_customer'))
customer_bp.add_url_rule('/customer/<int:id>/details/', view_func=CustomerDetailView.as_view('customer_details'))
customer_bp.add_url_rule('/api/customers', view_func=CustomerDataTableView.as_view('customer_data_table'))

customer_bp.add_url_rule('/api/customer-docs', view_func=CustomerDocsDataTableView.as_view('customer_docs_data_table'))
customer_bp.add_url_rule('/add-document', view_func=AddDocumentView.as_view('add_document'))
customer_bp.add_url_rule('/document/<int:id>/update/', view_func=UpdateDocumentView.as_view('update_document'))
customer_bp.add_url_rule('/document/<int:id>/delete/', view_func=DeleteDocumentView.as_view('delete_document'))

customer_bp.add_url_rule('/api/customer-contacts', view_func=CustomerContactsDataTableView.as_view('customer_contacts_data_table'))
customer_bp.add_url_rule('/add-contacts', view_func=AddContactsView.as_view('add_contacts'))
customer_bp.add_url_rule('/contact/<int:id>/update/', view_func=UpdateContactsView.as_view('update_contacts'))
customer_bp.add_url_rule('/contact/<int:id>/delete/', view_func=DeleteContactView.as_view('delete_contact'))


customer_bp.add_url_rule('/api/customer-billing-address', view_func=CustomerBillingAddDataTableView.as_view('customer_billing_add_data_table'))
customer_bp.add_url_rule('/add-billing-address', view_func=AddBillingAddView.as_view('add_billing_add'))
customer_bp.add_url_rule('/billing-address/<int:id>/update/', view_func=UpdateBillingAddressView.as_view('update_billing_address'))
customer_bp.add_url_rule('/billing-address/<int:id>/delete/', view_func=DeleteBillingAddressView.as_view('delete_billing_address'))


customer_bp.add_url_rule('/api/customer-shipping-address', view_func=CustomerShippingAddDataTableView.as_view('customer_shipping_add_data_table'))
customer_bp.add_url_rule('/add-shipping-address', view_func=AddShippingAddView.as_view('add_shipping_add'))
customer_bp.add_url_rule('/shipping-address/<int:id>/update/', view_func=UpdateShippingAddressView.as_view('update_shipping_address'))
customer_bp.add_url_rule('/shipping-address/<int:id>/delete/', view_func=DeleteShippingAddressView.as_view('delete_shipping_address'))