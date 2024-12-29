
from app import db
from flask.views import MethodView
from flask import Response, jsonify, redirect, render_template, request, url_for
from sqlalchemy import or_

from app.app_modules.base.base_views import BaseCreateView, BaseListView
from app.app_modules.products.models import Product
from app.app_modules.warehouse.models import Warehouse
from app.helper.utils import update_history_obj
from .models import Stock, StockHistory
from .forms import StockCreateForm

class CreateStockView(BaseCreateView):

    model = StockHistory
    form_class = StockCreateForm
    template_name = "stock/stock_form.html"

    def get_form_kwargs(self, **kwargs):
        kwargs = super().get_form_kwargs(**kwargs)
        kwargs['company_id'] = request.args.get('company_id')
        kwargs['product_id'] = request.args.get('product_id')
        return kwargs
    
    def get_context_data(self, form=None, **kwargs):
        ctx = super().get_context_data(form, **kwargs)
        product_id = request.args.get('product_id')
        ctx['total_stock'] = 0
        ctx['company_id'] = request.args.get('company_id')
        ctx['product_id'] = product_id
        return ctx


    def post(self, **kwargs):
        company_id = request.form.get('company_id')
        product_id = request.form.get('product_id')
        form = self.form_class(request.form, company_id=int(company_id),product_id=int(product_id))
        try:
            if form.validate_on_submit():
                new_stock = self.model(
                    product_id = request.form.get('product_id'),
                    warehouse_id = form.warehouse_id.data,
                    zone_id = form.zone_id.data,
                    vendor_id = form.vendor_id.data,
                    product_case_id = form.product_case_id.data,
                    no_of_case = form.no_of_case.data,
                    affected_stock = form.affected_stock.data,
                    per_piece_price = form.per_piece_price.data,
                    total_amount = form.total_amount.data,
                    manufacture_date = form.manufacture_date.data,
                    expiry_date = form.expiry_date.data,
                )
                modified_by_id = form.modified_by_id.data
                if modified_by_id > 0:
                    new_stock.modified_by_id = modified_by_id
                
                stock_obj = Stock.query.filter_by(product_id=product_id,company_id = company_id).first()

                if not stock_obj:
                    stock_obj = Stock(product_id=product_id,company_id = company_id)
                    new_stock.before_stock = stock_obj.total_stock
                    stock_obj.total_stock = int(form.affected_stock.data)
                else:
                    new_stock.before_stock = stock_obj.total_stock
                    stock_obj.total_stock += int(form.affected_stock.data)

                db.session.add(new_stock)
                db.session.commit()

                stock_obj.warehouse_id = form.warehouse_id.data
                stock_obj.vendor_id = form.vendor_id.data
                db.session.add(stock_obj)
                db.session.commit()

                update_history_obj(new_stock.id)

                return jsonify({'status': 'success', 'message': 'Stock created successfully!'}), 200
            else:
                return jsonify({'status': 'error', 'errors': form.errors}), 400

        except Exception as e:
            db.session.rollback()
            return jsonify({'status': 'error', 'message': 'An error occurred while processing the form.'}), 500


class StockDataTableView(MethodView):

    def _get_actions(self, obj):
        detail_url = "#"
        
        return (
            f'<div><span class="log_history_model mx-1" data-product_id="{obj.product.id}" data-id="{ obj.id }"'
            + f' title="History" data-bs-target="#myModal" data-bs-toggle="modal"><i class="fa fa-history text-success" style="cursor:pointer;"></i></span>'
            + f'<a href="{detail_url}" title="Detail"><i class="fa fa-eye font-medium-3"></i></a></div>'
        )

    def get(self):
        from sqlalchemy import cast, String

        product_id = request.args.get('product_id')
        company_id = request.args.get('company_id')
        search = request.args.get('search[value]')

        query = Stock.query.order_by(-Stock.id)
        if product_id:
            query = query.filter(Stock.product_id == product_id)
        if company_id:
            query = query.filter(Stock.company_id == company_id)
        if search:
            query = query.filter(
                or_(
                    Stock.product.has(Product.name.ilike(f'%{search}%')),
                    Stock.warehouse.has(Warehouse.name.ilike(f'%{search}%')),
                    Stock.product.has(Product.code.ilike(f'%{search}%'))
                )
            )
            

        start = int(request.args.get('start', 0))
        length = int(request.args.get('length', 10))
        stocks = query.offset(start).limit(length).all()

        data = []
        for index, stock in enumerate(stocks,start=1):
            data.append({
                "id": index,
                "product_code": stock.product.code,
                "product": stock.product.name,
                "available_stock": 0,
                "locked_quantity": 0,
                "actions": self._get_actions(stock)
            })

        return jsonify({
            "draw": int(request.args.get('draw', 1)),
            "recordsTotal": Stock.query.count(),
            "recordsFiltered": query.count(),
            "data": data
        })