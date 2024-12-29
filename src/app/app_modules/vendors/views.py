from app import db
from sqlalchemy import or_
from .models import Vendor
from .forms import VendorForm
from flask.views import MethodView
from ..company.models import Company
from flask import jsonify, render_template, request, url_for
from app.app_modules.base.base_views import BaseCreateView, BaseListView

class VendorListView(BaseListView):
    model = Vendor
    template_name = "vendor/vendor_list.html"

    def get_context_data(self,**kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["company_list"] = Company.query.order_by(Company.id) 
        return ctx

class DeleteVendor(MethodView):
    
    def post(self, id):
        vendor_obj = Vendor.query.get_or_404(id)
        try:
            db.session.delete(vendor_obj)
            db.session.commit()
            return jsonify({'message': 'Vendor deleted successfully.'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': str(e)}), 500
  
class CreateVendorView(BaseCreateView):

    model = Vendor
    form_class = VendorForm
    template_name = "vendor/vendor_create.html"

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
                vendor_obj = Vendor(
                    email = form.email.data,
                    status = form.status.data if form.status.data else Vendor.ACTIVE,
                    company_id = form.company_id.data,
                    full_name = form.full_name.data,
                    website = form.website.data,
                    address_line_1 = form.address_line_1.data,
                    address_line_2 = form.address_line_2.data,
                    state = form.state.data,
                    city = form.city.data,
                    phone = form.phone.data,
                    zip_code = form.zip_code.data,
                    country = form.country.data,
                )
                db.session.add(vendor_obj)
                db.session.commit()

                return jsonify({'status': 'success', 'message': 'Vendor created successfully!'}), 200
            except Exception as e:
                db.session.rollback()
                return jsonify({'status': 'error', 'errors': form.errors}), 400
        else:
            return jsonify({'status': 'error', 'errors': form.errors}), 400
        
class VendorUpdateView(MethodView):
    def get(self, id):
        vendor_obj = Vendor.query.get_or_404(id)
        form = VendorForm(obj=vendor_obj)
        return render_template("vendor/vendor_update.html", form=form,instance=vendor_obj)

    def post(self, id):
        vendor_obj = Vendor.query.get_or_404(id)
        form = VendorForm(request.form, obj=vendor_obj)
        if form.validate_on_submit():
            try:
                form.populate_obj(vendor_obj)
                db.session.commit()
                return jsonify({'status': 'success', 'message': 'Vendor updated successfully!'}), 200
            except Exception as e:
                db.session.rollback()
                return jsonify({'status': 'error', 'errors': form.errors}), 400
        return jsonify({'status': 'error', 'errors': form.errors}), 400

class VendorDetailsView(MethodView):
    model = Vendor
    template_name = "vendor/vendor_details.html"

    def get(self,id):
        # vendor_payments = VendorPayments.objects.filter(vendor=self.object)
        vendor_payments = None
        return render_template(
            self.template_name,
            object = Vendor.query.get(id),
            vendor_payments = vendor_payments,
        )

class VendorDataTableView(MethodView):

    def _get_actions(self, obj):
        detail_url = url_for('vendor_bp.vendor_details', id=obj.id)
        update_url = url_for('vendor_bp.update_vendor', id=obj.id)
        delete_url = url_for('vendor_bp.delete_vendor', id=obj.id)
        return (
            f'<div class="row"><center><a href="{detail_url}" class="vendor-details-btn" data-id="{obj.id}"'
            ' title="Detail"><i class="fa fa-eye font-medium-3 mx-1" style="margin-right: 10px;"></i></a><a'
            f' href="javascript:void(0)" title="Edit"><i data-url="{update_url}" class="fa fa-edit font-medium-3 mx-1 update_vendor" style="margin-right:'
            f' 10px;"></i></a> <label style="cursor: pointer;" data-title="{obj.full_name}"'
            f' data-url="{delete_url}" data-id="{obj.id}" title="Delete" class="danger p-0 delete-btn"><i'
            ' class="text-danger fa fa-trash font-medium-3"></i></label></center></div>'
        )
    
    def _get_purchase_order_count(self,obj):
        # total_order = PurchaseOrder.objects.filter(vendor=obj).aggregate(total_count=Count("id"))["total_count"]
        # return total_order if total_order else 0  
        return 0

    def _get_purchase_quantity(self,obj):
        # total_count = PurchaseOrderProducts.objects.filter(purchase_order__vendor=obj).aggregate(total_qty=Sum("total_pieces"))["total_qty"]
        # return total_count if total_count else 0
        return 0
    
    def _get_profit(self, obj):
        # product_id_list = list(StockHistory.objects.filter(vendor = obj).values_list("product", flat=True))
        # order_product_id_list = list(OrderProduct.objects.filter(product__id__in = product_id_list).values_list("id", flat=True))

        # return calculate_profit_order_product_wise(order_product_id_list)
        return 0

 

    def get(self):
        query = Vendor.query.order_by(-Vendor.id) 
        company_id = request.args.get('company')
        role = request.args.get('role')
        search = request.args.get('search[value]')

        if company_id:
            query = query.filter(Vendor.company_id == company_id)
        if role:
            query = query.filter(Vendor.company_id == company_id)
        if search:
            query = query.filter(
                or_(
                    Vendor.full_name.ilike(f'%{search}%'),
                    Vendor.status.ilike(f'%{search}%'),
                    Vendor.email.ilike(f'%{search}%'),
                    Vendor.city.ilike(f'%{search}%'),
                    Vendor.country.ilike(f'%{search}%'),
                    Vendor.state.ilike(f'%{search}%'),
                    Vendor.website.ilike(f'%{search}%'),
                )
            )

        start = int(request.args.get('start', 0))
        length = int(request.args.get('length', 10))
        vendors = query.offset(start).limit(length).all()

        data = []
        for index, o in enumerate(vendors,start=1):
            data.append({
                "id": index,
                "email": o.email,
                "purchase_order": self._get_purchase_order_count(o),
                "total_quantity": self._get_purchase_quantity(o),
                "profit": self._get_profit(o),
                "purchase_date": o.created_at.strftime("%d %b, %Y"),
                "full_name": o.full_name.title(),
                "phone": o.phone if o.phone else "-----",
                "city": o.city.title(),
                "actions": self._get_actions(o),
            })

        return jsonify({
            "draw": int(request.args.get('draw', 1)),
            "recordsTotal": Vendor.query.count(),
            "recordsFiltered": query.count(),
            "data": data
        })
    
class VendorPurchaseOrderDatatableList(MethodView):
    pass

class GetVendors(MethodView):
    def get(self):
        company_id = request.args.get('company_id')
        qs = Vendor.query.filter_by(company_id=company_id)

        default_option = {
            "id": "", 
            "text": "All",
        }

        vendor_list = [
            default_option  
        ] + [
            {
                "id": vendor.id,
                "text": vendor.full_name,
            }
            for vendor in qs.all()
        ]
        return jsonify({'vendors': vendor_list})