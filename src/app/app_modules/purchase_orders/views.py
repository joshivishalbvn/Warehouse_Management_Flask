import os
from app import db
from sqlalchemy import or_
from flask.views import MethodView
from .models import PurchaseOrder
from ..vendors.models import Vendor
from collections import defaultdict
from ..company.models import Company
from .models import PurchaseOrderProducts
from ..base.base_views import BaseListView
from werkzeug.utils import secure_filename
from werkzeug.datastructures import ImmutableMultiDict
from flask import jsonify, redirect, render_template, request, url_for
from .forms import PurchaseOrderCreateForm,PurchaseOrderProductForm,MultiplePurchaseOrderProductForm

class ProductListView(BaseListView):
    
    template_name = "purchase_order/purchase_order_list.html"
    model = PurchaseOrder

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company_list'] = Company.query.order_by(Company.id)
        context["vendor_list"] = Vendor.query.order_by(Vendor.id)
        return context
    
     
class PurchaseOrderDataTableView(MethodView):

    def _get_actions(self, obj):
        update_url = url_for('product_bp.update_product_case', id=obj.id)
        delete_url = url_for('product_bp.delete_product_case', id=obj.id)
        return f"<div class='text-center'><span data-url='{update_url}' title='Edit' class='update_this_case' style='color:var(--primary-bg-color); cursor: pointer;'><i class='fa fa-edit'></i></span> <label data-title='{obj.id}' data-id='{obj.id}' title='Delete' data-url='{delete_url}' class='text-danger delete-btn text-center'><i class='fa fa-trash'></i></label></div>"

    def get(self):
        from sqlalchemy import cast, String , func

        vendor_id = request.args.get('vendor_id')
        company_id = request.args.get('company_id')
        status = request.args.get("status")
        search = request.args.get('search[value]')

        query = PurchaseOrder.query.order_by(-PurchaseOrder.id)
        if vendor_id:
            query = query.filter(PurchaseOrder.vendor_id == vendor_id)
        if company_id:
            query = query.filter(PurchaseOrder.company_id == company_id)
        if status:
            query = query.filter(PurchaseOrder.status == status)
        if search:
            search_term = '%{}%'.format(search)
            query = query.filter(
                or_(
                    Vendor.full_name.ilike(search_term),
                    PurchaseOrder.purchase_id.ilike(search_term),
                    cast(PurchaseOrder.created_at, String).ilike(search_term),
                    PurchaseOrder.status.ilike(search_term),
                    cast(PurchaseOrder.total_price, String).ilike(search_term) 
                )
            )

        start = int(request.args.get('start', 0))
        length = int(request.args.get('length', 10))
        purchase_orders = query.offset(start).limit(length).all()

        data = []
        for index, purchase_order in enumerate(purchase_orders,start=1):
            total_quantity = (
                db.session.query(func.sum(PurchaseOrderProducts.case_quantity))
                .filter(PurchaseOrderProducts.purchase_order_id == purchase_order.id)
                .scalar()
            )

            data.append({
                "id": index,
                "purchase_id": purchase_order.purchase_id or "---",
                "created_at": purchase_order.created_at.strftime("%d %b, %Y"),
                "vendor": purchase_order.vendor.full_name,
                "total_products": len(purchase_order.purchase_order_products),
                "total_quantity": total_quantity or 0,
                "total_price": purchase_order.total_price,
                "actions": self._get_actions(purchase_order)
            })

        return jsonify({
            "draw": int(request.args.get('draw', 1)),
            "recordsTotal": PurchaseOrder.query.count(),
            "recordsFiltered": query.count(),
            "data": data
        })



def extract_form_data(form_data):
    main_form_data = {}
    purchase_order_products = defaultdict(dict)

    for key, value in form_data.items():
        if key.startswith('purchase_order_products'):
            parts = key.split('[')
            index = int(parts[1].split(']')[0])
            field_name = parts[2].split(']')[0]
            purchase_order_products[index][field_name] = value
        else:
            main_form_data[key] = value

    purchase_order_products_list = [purchase_order_products[i] for i in sorted(purchase_order_products.keys())]
    return ImmutableMultiDict(main_form_data), purchase_order_products_list


class PurchaseOrderCreateView(MethodView):
    template_name = "purchase_order/purchase_order_create.html"
    form_class = PurchaseOrderCreateForm
    inline_form_class = MultiplePurchaseOrderProductForm

    def get(self):
        form = self.form_class()
        inline_formset = self.inline_form_class()
        return render_template(self.template_name, form=form, inline_formset=inline_formset)

    def post(self):
        form_data = request.form
        file_data = request.files
        main_form_data, purchase_order_products_list = extract_form_data(form_data)
        form = PurchaseOrderCreateForm(formdata=main_form_data)

        if form.validate_on_submit():
            purchase_order = PurchaseOrder(
                company_id=form.company_id.data,
                vendor_id=form.vendor_id.data,
                total_price=form.total_price.data,
                remarks=form.remarks.data
            )
            db.session.add(purchase_order)
            db.session.flush()

            if 'invoice' in file_data:
                invoice = file_data['invoice']
                if invoice and allowed_file(invoice.filename):
                    filename = secure_filename(invoice.filename)
                    if not os.path.exists(PurchaseOrder.INVOICE_PATH):
                        os.makedirs(PurchaseOrder.INVOICE_PATH)
                    filepath = os.path.join(PurchaseOrder.INVOICE_PATH, filename)
                    invoice.save(filepath)
                    purchase_order.invoice = filename

            has_errors = False

            for product_data in purchase_order_products_list:
                product_form = PurchaseOrderProductForm(data=product_data)

                if product_form.validate():
                    product_data = PurchaseOrderProducts(
                        product_id=product_form.product_id.data,
                        case_size_id=product_form.case_size_id.data,
                        case_quantity=product_form.case_quantity.data,
                        total_pieces=product_form.total_pieces.data,
                        per_piece_price=product_form.per_piece_price.data,
                        amount=product_form.amount.data,
                        purchase_order_id=purchase_order.id
                    )
                    db.session.add(product_data)
                    db.session.flush()
                else:
                    has_errors = True
                    form.errors.setdefault('products', []).append(product_form.errors)

            if not has_errors:
                if purchase_order.id is not None:
                    purchase_order.purchase_id = "{}{:05d}".format("PO", purchase_order.id)
                db.session.commit()
                return redirect(url_for('po_bp.purchase_order'))

        return render_template(self.template_name, form=form, inline_formset=form.products)

    def render_error(self, form, inline_formset):
        return render_template(self.template_name, form=form, inline_formset=inline_formset), 400


def allowed_file(filename):
    allowed_extensions = {'pdf', 'jpg', 'jpeg', 'png'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions