from flask import Blueprint

from .views import CompanyListView, CreateCompany, UpdateCompany,CompanyDetailsView

company_bp = Blueprint('company_bp', __name__)

company_bp.add_url_rule('/companies', view_func=CompanyListView.as_view('company_list'))
company_bp.add_url_rule('/create-company', view_func=CreateCompany.as_view('create_company'))
company_bp.add_url_rule('/<int:id>/update-company', view_func=UpdateCompany.as_view('update_company'))
company_bp.add_url_rule('/<int:id>/company-details', view_func=CompanyDetailsView.as_view('company_details'))



