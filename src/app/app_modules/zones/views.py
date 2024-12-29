
from app import db
from .models import Zone
from sqlalchemy import or_
from .forms import ZoneForm
from flask.views import MethodView
from app.app_modules.base.base_views import BaseCreateView
from flask import jsonify, render_template, request, url_for



class DeleteZone(MethodView):
    
    def post(self, id):
        try:
            zone_obj = Zone.query.get_or_404(id)
            db.session.delete(zone_obj)
            db.session.commit()
            return jsonify({'message': 'Zone deleted successfully.'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': str(e)}), 500
        
class GetZoneAjax(MethodView):
    def get(self):
        warehouse_id = request.args.get('warehouse_id')
        zones = Zone.query.filter_by(warehouse_id=warehouse_id).all()
        default_option = {
            "id": "", 
            "text": "Please Select Zone",
        }

        zone_list = [
            default_option  
        ] + [
            {
                "id": zone.id,
                "name": zone.name,
            }
            for zone in zones
        ]
        
        return jsonify({'zones': zone_list})
  
class CreateZoneView(BaseCreateView):

    model = Zone
    form_class = ZoneForm
    template_name = "zone/zone_create.html"

    def get(self, **kwargs):
        form = self.form_class(**self.get_form_kwargs())
        context = self.get_context_data(form=form, **kwargs)
        if self.template_name:
            return render_template(self.template_name, **context)
        return jsonify({'message': 'GET request received'})

    def post(self, **kwargs):
        form = self.form_class(request.form, **self.get_form_kwargs())
        if form.validate_on_submit():
            try:
                zone_obj = Zone(
                    name = form.name.data,
                    status = form.status.data if form.status.data else Zone.ACTIVE,
                    warehouse_id = form.warehouse_id.data
                )
                db.session.add(zone_obj)
                db.session.commit()

                return jsonify({'status': 'success', 'message': 'Zone created successfully!'}), 200
            except Exception as e:
                db.session.rollback()
                return jsonify({'status': 'error', 'errors': form.errors}), 400
        else:
            return jsonify({'status': 'error', 'errors': form.errors}), 400
        
class ZoneUpdateView(MethodView):
    def get(self, id):
        zone_obj = Zone.query.get_or_404(id)
        form = ZoneForm(obj=zone_obj)
        return render_template("zone/zone_update.html", form=form,instance=zone_obj)

    def post(self, id):
        zone_obj = Zone.query.get_or_404(id)
        form = ZoneForm(request.form, obj=zone_obj,zone_id=zone_obj.id)
        if form.validate_on_submit():
            try:
                form.populate_obj(zone_obj)
                db.session.commit()
                return jsonify({'status': 'success', 'message': 'User updated successfully!'}), 200
            except Exception as e:
                db.session.rollback()
                return jsonify({'status': 'error', 'errors': form.errors}), 400
        return jsonify({'status': 'error', 'errors': form.errors}), 400
    

class ZoneDataTableView(MethodView):

    def _get_actions(self, obj):
        update_url = url_for('zone_bp.update_zone', id=obj.id)
        delete_url = url_for('zone_bp.delete_zone', id=obj.id)
        return f"<span data-url='{update_url}' title='Edit' class='zone_update' style='color:var(--primary-bg-color); cursor: pointer;'><i class='fa fa-edit'></i></span> <label data-title='{obj.name}' data-id='{obj.id}' title='Delete' data-url='{delete_url}' class='text-danger delete-btn text-center'><i class='fa fa-trash'></i></label>"
    
    def _get_status(self, obj):
        html_content = render_template("zone/get_zone_status.html",zone= obj)
        return html_content

    def _get_products(self, obj):
        stock_list = []
        is_stock_found = len(stock_list) > 0
        html_content = render_template('zone/zone_product_list.html', stock_list=stock_list, is_stock_found=is_stock_found)
        return html_content

    def get(self):
        query = Zone.query.order_by(Zone.id) 
        company_id = request.args.get('company')
        warehouse_id = request.args.get('warehouse')
        search = request.args.get('search[value]')

        if company_id:
            from ..warehouse.models import Warehouse
            query = query.filter(Zone.warehouse.has(Warehouse.company_id == company_id))
        if warehouse_id:
            query = query.filter(Zone.warehouse_id == warehouse_id)
        if search:
            query = query.filter(
                or_(
                    Zone.name.ilike(f'%{search}%'),
                    Zone.status.ilike(f'%{search}%'),
                )
            )

        start = int(request.args.get('start', 0))
        length = int(request.args.get('length', 10))
        zones = query.offset(start).limit(length).all()

        data = []
        for index, zone in enumerate(zones,start=1):
            data.append({
                "id": index,
                "name": zone.name,
                "warehouse_name": zone.warehouse.name,
                "status": self._get_status(zone),
                "products": self._get_products(zone),
                "actions": self._get_actions(zone),
            })

        return jsonify({
            "draw": int(request.args.get('draw', 1)),
            "recordsTotal": Zone.query.count(),
            "recordsFiltered": query.count(),
            "data": data
        })