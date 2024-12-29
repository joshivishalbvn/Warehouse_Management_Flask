from app import db
from sqlalchemy import or_
from .forms import BarcodeCreateForm, ImportProductCSVForm, ProductCaseForm, ProductForm
from flask.views import MethodView
from ..company.models import Company
from datetime import date, timedelta
from ...helper.utils import generate_barcode, save_csv, save_image, update_barcode
from .tasks import import_product_from_csv
from .models import Barcode, CSVFile, Product, ProductCase, ProductImage
from flask import jsonify, redirect, render_template, request, url_for
from app.app_modules.base.base_views import BaseCreateView, BaseListView

class ProductListView(BaseListView):
    
    model = Product
    template_name = "product/product_list.html"

    def get_context_data(self,**kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["products"] = Product.query.all()
        ctx["company_list"] = Company.query.order_by(Company.id) 
        return ctx
    
class CreateProduct(BaseCreateView):
    model = Product
    form_class = ProductForm
    template_name = "product/product_create.html"
    message = "Product Created Successfully..."

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
                product_obj = Product(
                    name=form.name.data,
                    code=form.code.data,
                    status=form.status.data,
                    company_id=form.company_id.data
                )
                db.session.add(product_obj)
                db.session.commit()
                try:
                    if 'product_image' in request.files:
                        image = request.files['product_image']
                        file_path = save_image(image)
                        product_img_obj = ProductImage(image_url=file_path,product_id=product_obj.id)
                        db.session.add(product_img_obj)
                        db.session.commit()
                except Exception:
                    pass

                return jsonify({'status': 'success', 'message': 'Product created successfully!'}), 200

            except Exception as e:
                db.session.rollback()
                return jsonify({'status': 'error', 'errors': form.errors}), 400

        else:
            return jsonify({'status': 'error', 'errors': form.errors}), 400
        
class ProductDataTableView(MethodView):

    def _get_actions(self, obj):
        update_url = url_for('product_bp.update_product', id=obj.id)
        delete_url = url_for('product_bp.delete_product', id=obj.id)
        barcode_url = url_for('product_bp.product_details', id=obj.id)

        return f"<a href='{barcode_url}' title='Detail' class='mx-1'><i class='fa fa-eye font-medium-3'></i></a><span data-url='{update_url}' title='Edit' class='update_product' style='color:var(--primary-bg-color); cursor: pointer;''><i class='fa fa-edit'></i></span> <label data-title='{obj.name}' data-id='{obj.id}' title='Delete' data-url='{delete_url}' class='text-danger delete-btn text-center'><i class='fa fa-trash'></i></label>"
        
    def _get_details_actions(self,obj):
        barcode_url = url_for('product_bp.product_details', id=obj.id)

        return f"<a href='{barcode_url}' title='Detail' class='mx-1 center-content'><i class='fa fa-eye  font-medium-3'></i></a>"
    
    def _get_product_image(self, obj):
        images = ProductImage.query.filter_by(product_id=obj.id).first()
        img_url = images.image_url if images else None
        html_content = render_template("product/get_product_image.html", height=80, img_url=img_url,obj=obj)
        return html_content
    
    def _get_product_info(self, obj):
        barcode_obj = Barcode.query.filter_by(product=obj).first()
        code_url = f"uploads/barcodes/{barcode_obj.code_url}" if barcode_obj else None
        html_content = render_template("product/get_product_info.html", product=obj, request=request,height=80,width=220,barcode_obj=barcode_obj,img_url=code_url if barcode_obj else "")
        return html_content

    def _get_product_stock_info(self, obj):
        case_size = ProductCase.query.filter_by(product_id=obj.id)
        # stock = Stock.objects.filter(product__id = obj.id).last()
        stock = None
        html_content = render_template("product/get_product_stock_info.html", product=obj, case_size=case_size,total_qty=stock.total_stock if stock else 0,locked_qty=stock.get_locked_stock if stock else 0,saleable_qty=(stock.total_stock - stock.get_locked_stock) if stock else 0,request=request,)
        return html_content
    
    def _get_product_cost_profit_info(self, obj):
        """product cost & profit information : purchase price, sale price , profit, margin"""

        # case_size = ProductCase.objects.filter(product__id=obj.id).last()
        case_size = None
        day_30 = date.today()-timedelta(days=30)
        day_90 = date.today()-timedelta(days=90)
        # day_30_qty = OrderProduct.objects.filter(product=obj,order__status=Order.DELIVERED ,created_at__date__gte=day_30).aggregate(total_qty=Sum("quantity"))["total_qty"]
        day_30_qty = 30
        # day_30_total = OrderProduct.objects.filter(product=obj,order__status=Order.DELIVERED ,created_at__date__gte=day_30).aggregate(item_total=Sum("item_total"))["item_total"]
        day_30_total = 30
        # day_90_qty = OrderProduct.objects.filter(product=obj,order__status=Order.DELIVERED ,created_at__date__gte=day_90).aggregate(total_qty=Sum("quantity"))["total_qty"]
        day_90_qty = 90
        # day_90_total = OrderProduct.objects.filter(product=obj,order__status=Order.DELIVERED ,created_at__date__gte=day_90).aggregate(item_total=Sum("item_total"))["item_total"]
        day_90_total = 90
        html_content = render_template(
            "product/get_product_cost_profit_info.html",
            product=obj,
            case_size=case_size,
            day_90_qty = day_90_qty if day_90_qty else 0,
            day_90_total = day_90_total if day_90_total else 0,
            day_30_qty =  day_30_qty if day_30_qty else 0,
            day_30_total = day_30_total if day_30_total else 0,
            request=request
        )
        return html_content
    
    def _get_image(self,obj):
        images = ProductImage.query.filter_by(product_id=obj.id).first()
        img_url = images.image_url if images else None
        html_content = render_template("product/prd_img.html", product=obj,img_url=img_url)
        return html_content
    
    def _get_total_price(self, obj):
        # product = ProductPrice.objects.filter(customer = self.customer_id).filter(product = obj).last()
        # if product:
        #     price = product.price
        # else:
        price = 0
        html_content = render_template("product/get_total_price.html", product=obj,price=price)
        return html_content

    def get_select_checkbox(self, obj):
        # customer_products = list(ProductPrice.objects.filter(customer = self.customer_id).values_list('product__id', flat=True))
        # if obj.id in customer_products:
        #     is_checked = True
        # else:
        is_checked = False
        html_content = render_template("action_buttons/product_code_with_checkbox.html", product=obj,is_checked=is_checked)
        return html_content

    def get(self):
        company_id = request.args.get('company')
        role = request.args.get('role')
        search = request.args.get('search[value]')

        query = Product.query.order_by(-Product.id) 
        if company_id:
            query = query.filter(Product.company_id == company_id)
        if role:
            query = query.filter(Product.role == role)
        if search:
            query = Product.query.join(Barcode, Product.barcodes).filter(
                or_(
                    Product.name.ilike(f'%{search}%'),
                    Product.code.ilike(f'%{search}%'),
                    Barcode.number.ilike(f'%{search}%')
                )
            ).order_by(Product.id.desc())

        start = int(request.args.get('start', 0))
        length = int(request.args.get('length', 10))
        products = query.offset(start).limit(length).all()

        data = []
        for index, product in enumerate(products,start=1):
            data.append({
                "id": index,
                "name": product.name,
                "code": product.code,
                "quantity": 0,
                "product_image": self._get_product_image(product),
                "image": self._get_image(product),
                "product_info": self._get_product_info(product),
                "stock_info": self._get_product_stock_info(product),
                "company": product.company.name,
                "cost_profit_info": self._get_product_cost_profit_info(product),
                "get_code": self.get_select_checkbox(product),
                "total_price": self._get_total_price(product),
                "actions": self._get_actions(product),
                "details_action": self._get_details_actions(product),
            })

        return jsonify({
            "draw": int(request.args.get('draw', 1)),
            "recordsTotal": Product.query.count(),
            "recordsFiltered": query.count(),
            "data": data
        })
    
class ProductCreateFromCSVFormView(BaseCreateView):
    template_name = "product/import_product.html"
    form_class = ImportProductCSVForm
    success_url = "product_bp.product_list"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["is_order"] = False
        return context
    
    def post(self, **kwargs):
        form = self.form_class(request.form)
        if form.validate_on_submit():
            form = self.form_class(request.form)
            csv_file = request.files["csv_file"]
            file_url = save_csv(csv_file)
            csv_file_obj = CSVFile(csv_file_url=file_url)
            db.session.add(csv_file_obj)
            db.session.commit()
            import_product_from_csv.delay(csv_file_obj.id)
            return redirect(url_for(self.success_url))

        else:
            return render_template(self.template_name, form=form)
        
class ProductCasesDataTableView(MethodView):

    def _get_actions(self, obj):
        update_url = url_for('product_bp.update_product_case', id=obj.id)
        delete_url = url_for('product_bp.delete_product_case', id=obj.id)
        return f"<div class='text-center'><span data-url='{update_url}' title='Edit' class='update_this_case' style='color:var(--primary-bg-color); cursor: pointer;'><i class='fa fa-edit'></i></span> <label data-title='{obj.quantity} Qty, {obj.weight} Oz, {obj.cubic_meter_volume} CMV' data-id='{obj.id}' title='Delete' data-url='{delete_url}' class='text-danger delete-btn text-center'><i class='fa fa-trash'></i></label></div>"

    def get(self):
        from sqlalchemy import cast, String

        product_id = request.args.get('product_id')
        search = request.args.get('search[value]')

        query = ProductCase.query.order_by(-ProductCase.id)
        if product_id:
            query = query.filter(ProductCase.product_id == product_id)
        if search:
            query = query.filter(
                or_(
                    cast(ProductCase.weight, String).ilike(f'%{search}%'),
                    cast(ProductCase.quantity, String).ilike(f'%{search}%'),
                    cast(ProductCase.cubic_meter_volume, String).ilike(f'%{search}%'),
                )
            )

        start = int(request.args.get('start', 0))
        length = int(request.args.get('length', 10))
        cases = query.offset(start).limit(length).all()

        data = []
        for case in cases:
            data.append({
                "weight": case.weight,
                "quantity": case.quantity,
                "cubic_meter_volume": case.cubic_meter_volume,
                "stock": case.get_total_stock,
                "actions": self._get_actions(case)
            })

        return jsonify({
            "draw": int(request.args.get('draw', 1)),
            "recordsTotal": ProductCase.query.count(),
            "recordsFiltered": query.count(),
            "data": data
        })


class ProductUpdateView(MethodView):
    form_class = ProductForm
    
    def get(self, id):
        product = Product.query.get_or_404(id)
        form = self.form_class(obj=product)
        return render_template("product/product_update.html", form=form,product=product)

    def post(self, id):
        product_obj = Product.query.get_or_404(id)
        form = self.form_class(request.form, obj=product_obj,product_id=id)
        if form.validate_on_submit():
            try:
                form.populate_obj(product_obj)
                db.session.commit()
                return jsonify({'status': 'success', 'message': 'Product updated successfully!'}), 200
            
            except Exception as e:
                return jsonify({'status': 'error', 'errors': form.errors}), 400
        else:
            return jsonify({'status': 'error', 'errors': form.errors}), 400

class DeleteProduct(MethodView):
    def post(self, id):
        try:
            product_obj = Product.query.get_or_404(id)
            images = ProductImage.query.filter_by(product_id=product_obj.id)
            for image in images:
                db.session.delete(image)
                db.session.commit()
            db.session.delete(product_obj)
            db.session.commit()
            return jsonify({'message': 'Product deleted successfully.'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': str(e)}), 500

class ProductDetailView(MethodView):
    model = Product
    template_name = "product/product_details.html"

    def get(self, id):
        product = Product.query.get_or_404(id)
        
        if not product:
            return render_template("404.html"), 404

        product_images = ProductImage.query.filter_by(product_id=id).all()
        product_cases = ProductCase.query.filter_by(product_id=id).all()
        # barcode_obj = Barcode.query.filter_by(product_id=id).order_by(Barcode.created_at.desc()).first()
        barcode_obj = None

        sales_statics = None

        can_add_barcode = barcode_obj is None

        previous_product = Product.query.filter(Product.id < id).order_by(Product.id.desc()).first()
        next_product = Product.query.filter(Product.id > id).order_by(Product.id).first()

        previous_product_id = previous_product.id if previous_product else None
        next_product_id = next_product.id if next_product else None

        return render_template(
            self.template_name,
            product=product,
            product_images=product_images,
            sales_statics=sales_statics,
            product_cases=product_cases,
            can_add_barcode=can_add_barcode,
            previous_product_id=previous_product_id,
            next_product_id=next_product_id,
        )
    
class ProductBarcodeList(MethodView):
    pass

class CreateProductBarcode(BaseCreateView):
    model = Barcode
    form_class = BarcodeCreateForm
    template_name = "product/barcode_create.html"
    message = "Barcode Created Successfully..."

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
                number=form.number.data
                product_id=form.product_id.data
                barcode = generate_barcode(product_id=product_id, barcode_number=number)
                return jsonify({'status': 'success', 'message': 'Barcode created successfully!'}), 200

            except Exception as e:
                import traceback
                traceback.print_exc()
                db.session.rollback()
                return jsonify({'status': 'error', 'errors': form.errors}), 400

        else:
            return jsonify({'status': 'error', 'errors': form.errors}), 400

class CreateProductCase(BaseCreateView):
    model = Product
    form_class = ProductCaseForm
    template_name = "product/product_case_create.html"
    message = "Product Case Created Successfully..."

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
                product_case_obj = ProductCase(
                    weight=form.weight.data,
                    quantity=form.quantity.data,
                    cubic_meter_volume=form.cubic_meter_volume.data,
                    product_id=form.product_id.data
                )
                db.session.add(product_case_obj)
                db.session.commit()

                return jsonify({'status': 'success', 'message': 'Product case created successfully!'}), 200

            except Exception as e:
                db.session.rollback()
                return jsonify({'status': 'error', 'errors': form.errors}), 400

        else:
            return jsonify({'status': 'error', 'errors': form.errors}), 400
        

class ProductCaseUpdateView(MethodView):
    form_class = ProductCaseForm
    
    def get(self, id):
        product_case = ProductCase.query.get_or_404(id)
        form = self.form_class(obj=product_case)
        return render_template("product/product_case_create.html", form=form,obj=product_case)

    def post(self, id):
        product_case = ProductCase.query.get_or_404(id)
        form = self.form_class(request.form, obj=product_case)
        if form.validate_on_submit():
            try:
                form.populate_obj(product_case)
                db.session.commit()
                return jsonify({'status': 'success', 'message': 'Product case updated successfully!'}), 200
            
            except Exception as e:
                return jsonify({'status': 'error', 'errors': form.errors}), 400
        else:
            return jsonify({'status': 'error', 'errors': form.errors}), 400

class ProductCaseDeleteView(MethodView):
    def post(self, id):
        try:
            case_obj = ProductCase.query.get_or_404(id)
            db.session.delete(case_obj)
            db.session.commit()
            return jsonify({'message': 'Product case deleted successfully.'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': str(e)}), 500
        

class ProductBarcodeDataTableView(MethodView):
    def _get_actions(self, obj):
        update_url = url_for('product_bp.update_product_barcode', id=obj.id)
        delete_url = url_for('product_bp.delete_product_barcode', id=obj.id)
        return f"<div class='text-center'><span data-url='{update_url}' title='Edit' class='update_this_case' style='color:var(--primary-bg-color); cursor: pointer;'><i class='fa fa-edit'></i></span> <label data-title='{obj.number}' title='Delete' data-url='{delete_url}' class='text-danger delete-btn text-center'><i class='fa fa-trash'></i></label></div>"
    
    def _get_barcode(self,obj):
        code_url = f"uploads/barcodes/{obj.code_url}"
        
        html_content = render_template("product/get_barcode_image.html", height= 80, width= 220, img_url = code_url, obj = obj,)
        return html_content

    def get(self):
        from sqlalchemy import cast, String

        product_id = request.args.get('product_id')
        search = request.args.get('search[value]')

        query = Barcode.query.order_by(-Barcode.id)
        if product_id:
            query = query.filter(Barcode.product_id == product_id)
        if search:
            query = query.filter(
                or_(
                    cast(Barcode.number, String).ilike(f'%{search}%'),
                )
            )

        start = int(request.args.get('start', 0))
        length = int(request.args.get('length', 10))
        barcodes = query.offset(start).limit(length).all()

        data = []
        for index, barcode in enumerate(barcodes,start=1):
            data.append({
                "id": index,
                "number": barcode.number,
                "barcode": self._get_barcode(barcode),
                "actions": self._get_actions(barcode)
            })

        return jsonify({
            "draw": int(request.args.get('draw', 1)),
            "recordsTotal": Barcode.query.count(),
            "recordsFiltered": query.count(),
            "data": data
        })
    

class ProductBarcodeUpdateView(MethodView):
    form_class = BarcodeCreateForm
    
    def get(self, id):
        barcode_obj = Barcode.query.get_or_404(id)
        form = self.form_class(obj=barcode_obj)
        return render_template("product/barcode_create.html", form=form,obj=barcode_obj)

    def post(self, id):
        barcode_obj = Barcode.query.get_or_404(id)
        form = self.form_class(request.form, obj=barcode_obj)
        if form.validate_on_submit():
            try:
                barcode = update_barcode(barcode_id=id, barcode_number=form.number.data)
                return jsonify({'status': 'success', 'message': 'Product barcode updated successfully!'}), 200
            
            except Exception as e:
                return jsonify({'status': 'error', 'errors': form.errors}), 400
        else:
            return jsonify({'status': 'error', 'errors': form.errors}), 400

class ProductBarcodeDeleteView(MethodView):
    def post(self, id):
        try:
            barcode_obj = Barcode.query.get_or_404(id)
            db.session.delete(barcode_obj)
            db.session.commit()
            return jsonify({'message': 'Product barcode deleted successfully.'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': str(e)}), 500
        
class GetProductsAjax(MethodView):
    def get(self):
        company_id = request.args.get('company_id')
        search = request.args.get('search')
        if company_id:
            qs = Product.query.filter_by(company_id = company_id, status = Product.ACTIVE)
        elif search:
            qs = Product.query.filter(
                Product.name.ilike(f'%{search}%') |
                Product.code.ilike(f'%{search}%') |
                Barcode.number.ilike(f'%{search}%')
            ).distinct()
        else:
            qs = Product.query

        default_option = {
            "id": "", 
            "text": "Search by product code, name and barcode",
        }

        product_list = [
            default_option  
        ] + [
            {
                "id": product.id,
                "text": f"({product.code}) {product.name}",
            }
            for product in qs.all()
        ]
        
        return jsonify({'products': product_list})
    
class ProductDetailsView(MethodView):
    def get(self):
        product_id = request.args.get("product_id")
        product = Product.query.filter_by(id=product_id, status=Product.ACTIVE).first()
        
        if not product:
            return jsonify({"error": "Product not found"}), 404
        
        case_packs = ""
        for case in product.cases:
            case_packs += f'{case.id}-{case.quantity}-{case.quantity} Qty, {case.weight} Oz, {case.cubic_meter_volume} CMV |'
        
        data = {
            "name": product.name,
            "code": product.code,
            "case_packs": case_packs,
        }

        return jsonify({"product_data": data})
    
class GetQuantityByCaseAjax(MethodView):
    def get(self):
        case_size_id = request.args.get('case_size_id')
        case_obj = ProductCase.query.get(case_size_id)
        return jsonify({'quantity': case_obj.quantity})