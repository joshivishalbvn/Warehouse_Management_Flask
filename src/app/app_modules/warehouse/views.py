
import random
import string
from flask import jsonify, render_template, request, url_for
from flask.views import MethodView
from sqlalchemy import or_
from app import db
from app.app_modules.company.models import Company
from .forms import WarehouseForm, WarehouseUpdateForm
from flask_login import current_user

from app.app_modules.base.base_views import BaseCreateView
from app.app_modules.users.models import User
from .models import Warehouse


class WareHouseList(MethodView):
    
    template_name = "warehouse/warehouse_list.html"

    def get(self):
        warehouses = Warehouse.query.order_by(Warehouse.id) 
        return render_template(self.template_name, warehouses=warehouses,warehouse_statuses=Warehouse.STATUS_CHOICES)


class CreateWarehouse(BaseCreateView):
    model = Warehouse
    form_class = WarehouseForm
    template_name = "warehouse/warehouse_create.html"
    message = "Warehouse Created Sucessfully..."


    def get(self, **kwargs):
        form = self.form_class()
        
        context = self.get_context_data(form=form, **kwargs)
        if self.template_name:
            return render_template(self.template_name, **context)
        return jsonify({'message': 'GET request received'})

    def post(self, **kwargs):
        form = self.form_class(request.form)
        if form.validate_on_submit():
            try:
                warehouse_obj = Warehouse(
                    name=form.name.data,
                    address_line_1=form.address_line_1.data,
                    address_line_2=form.address_line_2.data,
                    city=form.city.data,
                    state=form.state.data,
                    zip_code=form.zip_code.data,
                    country=form.country.data,
                    company_id=form.company_id.data
                )

                # if current_user.is_superuser:
                #     new_project.company_id = form.company_id.data  
                # else:
                #     new_project.company_id = company_id
                db.session.add(warehouse_obj)
                db.session.commit()
                return jsonify({'status': 'success', 'message': 'Warehouse created successfully!'}), 200
            except Exception as e:
                db.session.rollback()
                return jsonify({'status': 'error', 'errors': form.errors}), 400
        else:
            return jsonify({'status': 'error', 'errors': form.errors}), 400
    

class UpdateWarehouse(MethodView):
    def get(self, id):
        warehouse = Warehouse.query.get_or_404(id)
        form = WarehouseUpdateForm(obj=warehouse)
        return render_template("warehouse/warehouse_update.html", form=form,warehouse=warehouse)

    def post(self, id):
        warehouse_obj = Warehouse.query.get_or_404(id)
        form = WarehouseUpdateForm(request.form, obj=warehouse_obj)
        if form.validate_on_submit():
            try:
                form.populate_obj(warehouse_obj)
                db.session.commit()
                return jsonify({'status': 'success', 'message': 'Company updated successfully!'}), 200
            
            except Exception as e:
                return jsonify({'status': 'error', 'errors': form.errors}), 400
        else:
            return jsonify({'status': 'error', 'errors': form.errors}), 400
        
class WarehouseDetails(MethodView):
    def get(self, id):
        from ..zones.models import Zone
        return render_template(
            "warehouse/warehouse_details.html",
            warehouse=Warehouse.query.get_or_404(id),
            active_zones=Zone.query.filter_by(warehouse_id=id,status=Zone.ACTIVE).count(),
            inactive_zones=Zone.query.filter_by(warehouse_id=id,status=Zone.INACTIVE).count()
        )

class Loadmanager(MethodView):
    pass



class WarehouseDataTableView(MethodView):

    def _get_actions(self, obj):
        update_url = url_for('wh_bp.update_warehouse', id=obj.id)
        details_url = url_for('wh_bp.warehouse_details', id=obj.id)
        return f"<span data-url='{update_url}' title='Edit' class='update_this_warehouse' style='color:var(--primary-bg-color); cursor: pointer;''><i class='fa fa-edit'></i></span> <a href='{details_url}' title='Detail' class='mx-1'><i class='fa fa-eye font-medium-3'></i></a>"

    def _get_status(self, obj):
        html_content = render_template("warehouse/get_warehouse_status.html",warehouse= obj)
        return html_content
    
    def get(self):
        company_id = request.args.get('company')
        search = request.args.get('search[value]')

        query = Warehouse.query.order_by(Warehouse.id) 
        if company_id:
            query = query.filter(Warehouse.company_id == company_id)
        if search:
            query = query.filter(
            or_(
                Warehouse.name.ilike(f'%{search}%'),
                Warehouse.city.ilike(f'%{search}%'),
                Warehouse.state.ilike(f'%{search}%'),
                Warehouse.country.ilike(f'%{search}%'),
            )
        )

        start = int(request.args.get('start', 0))
        length = int(request.args.get('length', 10))
        warehouses = query.offset(start).limit(length).all()

        data = []
        for index, warehouse in enumerate(warehouses,start=1):
            data.append({
                "id": index,
                "name": warehouse.name.title(),
                "address":f'{warehouse.city } , { warehouse.state },{ warehouse.country }',
                "zones": 0,
                "products": 0,
                "status": self._get_status(warehouse),
                "actions": self._get_actions(warehouse),
            })

        return jsonify({
            "draw": int(request.args.get('draw', 1)),
            "recordsTotal": Warehouse.query.count(),
            "recordsFiltered": query.count(),
            "data": data
        })
