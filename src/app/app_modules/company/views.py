
import random
import string
from app import db
from flask.views import MethodView
from flask import jsonify, render_template, request

from .models import Company
from ..zones.models import Zone
from ..warehouse.models import Warehouse
from app.app_modules.users.models import User
from app.app_modules.base.base_views import BaseCreateView
from app.app_modules.company.forms import CompanyForm, CompanyUpdateForm


class CompanyListView(MethodView):
    
    template_name = "company/company_list.html"

    def get(self):
        companies = Company.query.order_by(Company.id) 
        return render_template(self.template_name, companies=companies,company_statuses = Company.STATUS_CHOICES)


class CreateCompany(BaseCreateView):
    model = Company
    form_class = CompanyForm
    template_name = "company/company_create.html"

    def post(self, **kwargs):
        form = self.form_class(request.form, **self.get_form_kwargs())
        if form.validate_on_submit():
            company_email = form.email.data
            try:
                company = Company(
                    name=form.name.data,
                    email=company_email,
                    phone=form.phone.data,
                    status=form.status.data,
                )
                logo = form.logo.data
                if logo:
                    company.set_logo(logo)
                
                db.session.add(company)
                db.session.commit()

                user_obj = User(email=company_email)
                password = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
                user_obj.role = User.COMPANY_ADMIN
                user_obj.first_name = company_email.split("@")[0]
                user_obj.set_password(password)
                user_obj.company_id = company.id
                db.session.add(user_obj)
                db.session.commit()

                return jsonify({'status': 'success', 'message': 'Company created successfully!'}), 200
            except Exception as e:
                db.session.rollback()
                return jsonify({'status': 'error', 'errors': form.errors}), 400
        else:
            return jsonify({'status': 'error', 'errors': form.errors}), 400
    

class UpdateCompany(MethodView):
    def get(self, id):
        company = Company.query.get_or_404(id)
        form = CompanyUpdateForm(obj=company)
        return render_template("company/company_update.html", form=form,company=company)

    def post(self, id):
        company_obj = Company.query.get_or_404(id)
        form = CompanyUpdateForm(request.form, obj=company_obj)
        if form.validate_on_submit():
            try:
                form.populate_obj(company_obj)
                db.session.commit()
                return jsonify({'status': 'success', 'message': 'Company updated successfully!'}), 200
            
            except Exception as e:
                return jsonify({'status': 'error', 'errors': form.errors}), 400
        else:
            return jsonify({'status': 'error', 'errors': form.errors}), 400
        
class CompanyDetailsView(MethodView):
    def get(self, id):
        company = Company.query.get_or_404(id)
        warehouses = Warehouse.query.filter_by(company_id=id).order_by(Warehouse.id) 
        zones = Zone.query.filter(Zone.warehouse.has(company_id=id)).order_by(Zone.id).all()

        form = CompanyUpdateForm(obj=company)
        return render_template("company/company_details.html", form=form,company=company,warehouses=warehouses,zones=zones)