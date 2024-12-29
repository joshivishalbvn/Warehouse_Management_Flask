from flask import Blueprint
from .views import CreateUserView, DeleteUser, UserDataTableView, UserUpdateView, UserListView , GetSalesRepresentativeAjax,EmployeeDataTableView
user_bp = Blueprint('user_bp', __name__)

user_bp.add_url_rule('/users', view_func=UserListView.as_view('user_list'))
user_bp.add_url_rule('/user/<int:user_id>/delete/', view_func=DeleteUser.as_view('delete_user'))
user_bp.add_url_rule('/create-user', view_func=CreateUserView.as_view('create_user'))
user_bp.add_url_rule('/<int:id>/update-user', view_func=UserUpdateView.as_view('update_user'))
user_bp.add_url_rule('/api/users', view_func=UserDataTableView.as_view('user_data_table'))
user_bp.add_url_rule('/api/employees', view_func=EmployeeDataTableView.as_view('employee_data_table'))
user_bp.add_url_rule('/api/get-sales-representatives', view_func=GetSalesRepresentativeAjax.as_view('get_sales_representative_ajax'))
