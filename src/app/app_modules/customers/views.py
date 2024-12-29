import random
import string
from app import db
from ..users.models import User
from flask.views import MethodView
from ..company.models import Company
from flask import jsonify, render_template, request, url_for
from app.app_modules.base.base_views import BaseCreateView, BaseListView
from app.helper.utils import delete_document, save_document, update_document
from .forms import CustomerAddressForm, CustomerContactsForm, CustomerDocumentForm, CustomerForm
from .models import Customer, CustomerBillingAddress, CustomerDocuments, CustomerShippingAddress, MultipleCustomerPerson


class CustomerListView(BaseListView):
    
    model = Customer
    template_name = "customer/customer_list.html"

    def get_queryset(self):
        return Customer.query.all()

    def get_context_data(self,**kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["customers"] = Customer.query.all()
        ctx["company_list"] = Company.query.order_by(Company.id) 
        return ctx

class DeleteCustomer(MethodView):
    
    def post(self, id):
        try:
            customer_obj = Customer.query.get_or_404(id)
            user_obj = User.query.get(customer_obj.user_id)
            db.session.delete(user_obj)
            db.session.commit()
            db.session.delete(customer_obj)
            db.session.commit()
            return jsonify({'message': 'Customer deleted successfully.'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': str(e)}), 500
  
class CreateCustomerView(BaseCreateView):

    model = Customer
    form_class = CustomerForm
    template_name = "customer/customer_add.html"

    def post(self, **kwargs):
        form = self.form_class(request.form, **self.get_form_kwargs())
        if form.validate_on_submit():
            try:
                status=form.status.data,
                type=form.type.data,
                bill_to=form.bill_to.data,
                ship_to=form.ship_to.data,
                sales_representative_id=form.sales_representative_id.data

                company_id = form.company_id.data
                first_name = form.first_name.data
                last_name = form.last_name.data
                email = form.email.data

                """Managing User Model"""
                password = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
                customer_user = User(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                )
                customer_user.set_password(password)
                customer_user.role = User.CUSTOMER
                customer_user.company_id = company_id
                db.session.add(customer_user)
                db.session.commit()

                new_customer=Customer(
                    status=status,
                    type=type,
                    bill_to=bill_to,
                    ship_to=ship_to,
                    user_id=customer_user.id,
                    sales_representative_id=sales_representative_id
                )

                db.session.add(new_customer)
                db.session.commit()

                return jsonify({'status': 'success', 'message': 'Customer created successfully!'}), 200
            except Exception as e:
                db.session.rollback()
                return jsonify({'status': 'error', 'errors': form.errors}), 400
        else:
            return jsonify({'status': 'error', 'errors': form.errors}), 400
        
class AddDocumentView(BaseCreateView):

    model = CustomerDocuments
    form_class = CustomerDocumentForm
    template_name = "customer/add_documents.html"

    def post(self, **kwargs):
        form = self.form_class(request.form, **self.get_form_kwargs())
        if form.validate_on_submit():
            try:
                name = form.name.data
                customer_id = form.customer_id.data
                attachment = request.files['attachment']
                file_path = save_document(attachment)
                new_document = CustomerDocuments(
                    name = name,
                    attachment=file_path,
                    customer_id=customer_id
                )
                db.session.add(new_document)
                db.session.commit()
                return jsonify({'status': 'success', 'message': 'Customer created successfully!'}), 200
            except Exception as e:
                db.session.rollback()
                return jsonify({'status': 'error', 'errors': form.errors}), 400
        else:
            return jsonify({'status': 'error', 'errors': form.errors}), 400

class AddContactsView(BaseCreateView):

    model = MultipleCustomerPerson
    form_class = CustomerContactsForm
    template_name = "customer/create_contact_person.html"

    def post(self, **kwargs):
        form = self.form_class(request.form, **self.get_form_kwargs())
        if form.validate_on_submit():
            try:
                new_contact = MultipleCustomerPerson(
                    name = form.name.data,
                    email = form.email.data,
                    phone = form.phone.data,
                    customer_id = form.customer_id.data,
                )
                db.session.add(new_contact)
                db.session.commit()
                return jsonify({'status': 'success', 'message': 'Contact created successfully!'}), 200
            except Exception as e:
                db.session.rollback()
                return jsonify({'status': 'error', 'errors': form.errors}), 400
        else:
            return jsonify({'status': 'error', 'errors': form.errors}), 400

class AddBillingAddView(BaseCreateView):

    model = CustomerBillingAddress
    form_class = CustomerAddressForm
    template_name = "customer/billing_address.html"

    def post(self, **kwargs):
        form = self.form_class(request.form, **self.get_form_kwargs())
        if form.validate_on_submit():
            try:
                new_billing_obj = CustomerBillingAddress(
                    suite_apartment = form.suite_apartment.data,
                    address_line_1 = form.address_line_1.data,
                    address_line_2 = form.address_line_2.data,
                    city = form.city.data,
                    state = form.state.data,
                    country = form.country.data,
                    zip_code = form.zip_code.data,
                    latitude = form.latitude.data,
                    longitude = form.longitude.data,
                    is_default = form.is_default.data,
                    customer_id = form.customer_id.data,
                )
                db.session.add(new_billing_obj)
                db.session.commit()
                return jsonify({'status': 'success', 'message': 'Billing address created successfully!'}), 200
            except Exception as e:
                db.session.rollback()
                return jsonify({'status': 'error', 'errors': form.errors}), 400
        else:
            return jsonify({'status': 'error', 'errors': form.errors}), 400
        
class AddShippingAddView(BaseCreateView):

    model = CustomerShippingAddress
    form_class = CustomerAddressForm
    template_name = "customer/shipping_address.html"

    def post(self, **kwargs):
        form = self.form_class(request.form, **self.get_form_kwargs())
        if form.validate_on_submit():
            try:
                new_shipping_obj = self.model(
                    suite_apartment = form.suite_apartment.data,
                    address_line_1 = form.address_line_1.data,
                    address_line_2 = form.address_line_2.data,
                    city = form.city.data,
                    state = form.state.data,
                    country = form.country.data,
                    zip_code = form.zip_code.data,
                    latitude = form.latitude.data,
                    longitude = form.longitude.data,
                    is_default = form.is_default.data,
                    customer_id = form.customer_id.data,
                )
                db.session.add(new_shipping_obj)
                db.session.commit()
                return jsonify({'status': 'success', 'message': 'Shipping address created successfully!'}), 200
            except Exception as e:
                db.session.rollback()
                return jsonify({'status': 'error', 'errors': form.errors}), 400
        else:
            return jsonify({'status': 'error', 'errors': form.errors}), 400

class UpdateDocumentView(MethodView):
    form_class = CustomerDocumentForm

    def get(self, id):
        doc_obj = CustomerDocuments.query.get_or_404(id)
        form = self.form_class(obj=doc_obj)
        return render_template("customer/add_documents.html", form=form,instance=doc_obj)
    
    def post(self,id):
        doc_obj = CustomerDocuments.query.get_or_404(id)
        form = self.form_class(request.form, instance=doc_obj)
        if form.validate_on_submit():
            try:
                name = form.name.data
                customer_id = form.customer_id.data
                attachment = request.files['attachment']
                if attachment:
                    file_path = update_document(id,attachment)
                    doc_obj.attachment=file_path

                doc_obj.name = name
                doc_obj.customer_id=customer_id
                db.session.add(doc_obj)
                db.session.commit()
                return jsonify({'status': 'success', 'message': 'Document updated successfully!'}), 200
            except Exception as e:
                db.session.rollback()
                return jsonify({'status': 'error', 'errors': form.errors}), 400
        else:
            return jsonify({'status': 'error', 'errors': form.errors}), 400
        
class UpdateContactsView(MethodView):
    form_class = CustomerContactsForm

    def get(self, id):
        contact_obj = MultipleCustomerPerson.query.get_or_404(id)
        form = self.form_class(obj=contact_obj)
        return render_template("customer/create_contact_person.html", form=form,instance=contact_obj)
    
    def post(self,id):
        contact_obj = MultipleCustomerPerson.query.get_or_404(id)
        form = self.form_class(request.form, instance=contact_obj)
        if form.validate_on_submit():
            try:
                contact_obj.name = form.name.data
                contact_obj.email = form.email.data
                contact_obj.phone = form.phone.data
                contact_obj.customer_id = form.customer_id.data
                db.session.add(contact_obj)
                db.session.commit()
                return jsonify({'status': 'success', 'message': 'Contact updated successfully!'}), 200
            except Exception as e:
                db.session.rollback()
                return jsonify({'status': 'error', 'errors': form.errors}), 400
        else:
            return jsonify({'status': 'error', 'errors': form.errors}), 400
        
class UpdateBillingAddressView(MethodView):
    form_class = CustomerAddressForm

    def get(self, id):
        billing_obj = CustomerBillingAddress.query.get_or_404(id)
        form = self.form_class(obj=billing_obj)
        return render_template("customer/billing_address.html", form=form,instance=billing_obj)
    
    def post(self,id):
        billing_obj = CustomerBillingAddress.query.get_or_404(id)
        form = self.form_class(request.form, instance=billing_obj)
        if form.validate_on_submit():
            try:
                form.populate_obj(billing_obj)
                db.session.commit()
                db.session.commit()
                return jsonify({'status': 'success', 'message': 'Billing Address updated successfully!'}), 200
            except Exception as e:
                db.session.rollback()
                return jsonify({'status': 'error', 'errors': form.errors}), 400
        else:
            return jsonify({'status': 'error', 'errors': form.errors}), 400
        
class UpdateShippingAddressView(MethodView):
    form_class = CustomerAddressForm

    def get(self, id):
        shipping_obj = CustomerShippingAddress.query.get_or_404(id)
        form = self.form_class(obj=shipping_obj)
        return render_template("customer/shipping_address.html", form=form,instance=shipping_obj)
    
    def post(self,id):
        shipping_obj = CustomerShippingAddress.query.get_or_404(id)
        form = self.form_class(request.form, instance=shipping_obj)
        if form.validate_on_submit():
            try:
                form.populate_obj(shipping_obj)
                db.session.commit()
                db.session.commit()
                return jsonify({'status': 'success', 'message': 'Shipping Address updated successfully!'}), 200
            except Exception as e:
                db.session.rollback()
                return jsonify({'status': 'error', 'errors': form.errors}), 400
        else:
            return jsonify({'status': 'error', 'errors': form.errors}), 400
        
class DeleteDocumentView(MethodView):
    def post(self, id):
        try:
            doc_obj = CustomerDocuments.query.get_or_404(id)
            delete_document(id)
            db.session.delete(doc_obj)
            db.session.commit()
            return jsonify({'message': 'Document deleted successfully.'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': str(e)}), 500
        
class DeleteContactView(MethodView):
    def post(self, id):
        try:
            contact_obj = MultipleCustomerPerson.query.get_or_404(id)
            delete_document(id)
            db.session.delete(contact_obj)
            db.session.commit()
            return jsonify({'message': 'Contact deleted successfully.'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': str(e)}), 500

class DeleteBillingAddressView(MethodView):
    def post(self, id):
        try:
            add_obj = CustomerBillingAddress.query.get_or_404(id)
            delete_document(id)
            db.session.delete(add_obj)
            db.session.commit()
            return jsonify({'message': 'Billing Address deleted successfully.'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': str(e)}), 500
        
class DeleteShippingAddressView(MethodView):
    def post(self, id):
        try:
            add_obj = CustomerShippingAddress.query.get_or_404(id)
            delete_document(id)
            db.session.delete(add_obj)
            db.session.commit()
            return jsonify({'message': 'Shipping Address deleted successfully.'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': str(e)}), 500

class CustomerUpdateView(MethodView):
    def get(self, id):
        customer_obj = Customer.query.get_or_404(id)
        user_obj = User.query.get_or_404(customer_obj.user_id)  # Fetch the associated User object
        
        form = CustomerForm(obj=customer_obj)
        form.first_name.data = user_obj.first_name
        form.last_name.data = user_obj.last_name
        form.email.data = user_obj.email
        form.company_id.data = user_obj.company_id
        return render_template("customer/customer_add.html", form=form,instance=customer_obj)

    def post(self, id):
        customer_obj = Customer.query.get_or_404(id)
        form = CustomerForm(request.form, obj=customer_obj)
        if form.validate_on_submit():
            try:
                user_obj = User.query.get(customer_obj.user_id)
                user_obj.company_id = form.company_id.data
                user_obj.first_name = form.first_name.data
                user_obj.last_name = form.last_name.data
                user_obj.email = form.email.data
                db.session.add(user_obj)
                db.session.commit()

                customer_obj.status=form.status.data
                customer_obj.type=form.type.data,
                customer_obj.bill_to=form.bill_to.data,
                customer_obj.ship_to=form.ship_to.data,
                customer_obj.sales_representative_id=form.sales_representative_id.data,
                db.session.add(customer_obj)
                db.session.commit()

                return jsonify({'status': 'success', 'message': 'Customer created successfully!'}), 200
            except Exception as e:
                db.session.rollback()
                return jsonify({'status': 'error', 'errors': form.errors}), 400
        else:
            return jsonify({'status': 'error', 'errors': form.errors}), 400
    
from sqlalchemy import or_

class CustomerDataTableView(MethodView):

    def _get_actions(self, obj):
        detail_url = url_for('customer_bp.customer_details', id=obj.id)
        update_url = url_for('customer_bp.update_customer', id=obj.id)
        delete_url = url_for('customer_bp.delete_customer', id=obj.id)
        return (
            f'<div class="row"><center><a href="{detail_url}" class="customer-details-btn" data-id="{obj.id}"'
            ' title="Detail"><i class="fa fa-eye font-medium-3 mx-1" style="margin-right: 10px;"></i></a>'
            f'<a href="javascript:void(0)" title="Edit" data-url="{update_url}" class="update_customer'
            f' text-primary mx-1"><i class="fa fa-edit"></i></a>'
            f'<label style="cursor: pointer;" data-title="{obj.user.first_name} {obj.user.last_name}" data-url="{delete_url}"'
            f' data-id="{obj.id}" title="Delete" class="danger delete-btn"><i class="text-danger fa'
            ' fa-trash font-medium-3 "></i></label></center></div>'
        )

    def get(self):
        company_id = request.args.get('company')
        role = request.args.get('role')
        search = request.args.get('search[value]')

        query = Customer.query.order_by(Customer.id) 
        if company_id:
            query = query.filter(Customer.company_id == company_id)
        if role:
            query = query.filter(Customer.role == role)
        if search:
            query = query.filter(
                or_(
                    Customer.type.ilike(f'%{search}%'),
                )
            )

        start = int(request.args.get('start', 0))
        length = int(request.args.get('length', 10))
        customers = query.offset(start).limit(length).all()

        data = []
        for index, customer in enumerate(customers,start=1):
            data.append({
                "id": index,
                "full_name": f"{customer.user.first_name.title()} {customer.user.last_name.title()}",
                "email": customer.user.email,
                "type": customer.type,
                "total_orders": 0,
                "total_orders_amount": 0,
                "profit": 0,
                "margin": 0,
                "last_order_date": 0,
                "status": 0,
                "actions": self._get_actions(customer),
            })

        return jsonify({
            "draw": int(request.args.get('draw', 1)),
            "recordsTotal": Customer.query.count(),
            "recordsFiltered": query.count(),
            "data": data
        })

class CustomerContactsDataTableView(MethodView):
    def _get_actions(self, obj):
        update_url = url_for('customer_bp.update_contacts', id=obj.id)
        delete_url = url_for('customer_bp.delete_contact', id=obj.id)
        return (
            f'<div class="row"><center>'
            f'<a href="javascript:void(0)" title="Edit" data-url="{update_url}" class="update_element'
            f' text-primary mx-1"><i class="fa fa-edit"></i></a>'
            f'<label style="cursor: pointer;" data-title="{obj.name}" data-url="{delete_url}"'
            f' data-id="{obj.id}" data-table="#contacts_table"  data-text="Contact Deleted Successfully !!!" title="Delete" class="danger delete-btn"><i class="text-danger fa'
            ' fa-trash font-medium-3 "></i></label></center></div>'
        )
    

    def get(self):
        customer_id = request.args.get('customer_id')
        search = request.args.get('search[value]')

        query = MultipleCustomerPerson.query.order_by(MultipleCustomerPerson.id) 
        if customer_id:
            query = query.filter(MultipleCustomerPerson.customer_id == customer_id)
        if search:
            query = query.filter(
                or_(
                    MultipleCustomerPerson.name.ilike(f'%{search}%'),
                )
            )

        start = int(request.args.get('start', 0))
        length = int(request.args.get('length', 10))
        contacts = query.offset(start).limit(length).all()

        data = []
        for index, contact in enumerate(contacts,start=1):
            data.append({
                "id": index,
                "name": contact.name,
                "email": contact.email,
                "phone": contact.phone,
                "actions": self._get_actions(contact),
            })

        return jsonify({
            "draw": int(request.args.get('draw', 1)),
            "recordsTotal": MultipleCustomerPerson.query.count(),
            "recordsFiltered": query.count(),
            "data": data
        })
    
class CustomerBillingAddDataTableView(MethodView):
    def _get_actions(self, obj):
        update_url = url_for('customer_bp.update_billing_address', id=obj.id)
        delete_url = url_for('customer_bp.delete_billing_address', id=obj.id)
        return (
            f'<div class="row"><center>'
            f'<a href="javascript:void(0)" title="Edit" data-url="{update_url}" class="update_element'
            f' text-primary mx-1"><i class="fa fa-edit"></i></a>'
            f'<label style="cursor: pointer;" data-title="{obj.country}" data-url="{delete_url}"'
            f' data-id="{obj.id}" data-table="#billing_add_table"  data-text="Billing Address Deleted Successfully !!!" title="Delete" class="danger delete-btn"><i class="text-danger fa'
            ' fa-trash font-medium-3 "></i></label></center></div>'
        )
    

    def get(self):
        customer_id = request.args.get('customer_id')
        search = request.args.get('search[value]')

        query = CustomerBillingAddress.query.order_by(CustomerBillingAddress.id) 
        if customer_id:
            query = query.filter(CustomerBillingAddress.customer_id == customer_id)
        if search:
            query = query.filter(
                or_(
                    CustomerBillingAddress.address_line_1.ilike(f'%{search}%'),
                    CustomerBillingAddress.address_line_2.ilike(f'%{search}%'),
                    CustomerBillingAddress.suite_apartment.ilike(f'%{search}%'),
                    CustomerBillingAddress.city.ilike(f'%{search}%'),
                    CustomerBillingAddress.state.ilike(f'%{search}%'),
                    CustomerBillingAddress.country.ilike(f'%{search}%'),
                )
            )

        start = int(request.args.get('start', 0))
        length = int(request.args.get('length', 10))
        addresses = query.offset(start).limit(length).all()

        data = []
        for index, address in enumerate(addresses,start=1):
            data.append({
                "id": index,
                "address": f"{address.city.title()},{address.state.title()},{address.country.title()}",
                "default": "Yes"  if address.is_default else "No",
                "actions": self._get_actions(address),
            })

        return jsonify({
            "draw": int(request.args.get('draw', 1)),
            "recordsTotal": CustomerBillingAddress.query.count(),
            "recordsFiltered": query.count(),
            "data": data
        })
    
class CustomerShippingAddDataTableView(MethodView):
    def _get_actions(self, obj):
        update_url = url_for('customer_bp.update_shipping_address', id=obj.id)
        delete_url = url_for('customer_bp.delete_shipping_address', id=obj.id)
        return (
            f'<div class="row"><center>'
            f'<a href="javascript:void(0)" title="Edit" data-url="{update_url}" class="update_element'
            f' text-primary mx-1"><i class="fa fa-edit"></i></a>'
            f'<label style="cursor: pointer;" data-title="{obj.country}" data-url="{delete_url}"'
            f' data-id="{obj.id}" data-table="#shipping_add"  data-text="Shipping Address Deleted Successfully !!!" title="Delete" class="danger delete-btn"><i class="text-danger fa'
            ' fa-trash font-medium-3 "></i></label></center></div>'
        )
    

    def get(self):
        customer_id = request.args.get('customer_id')
        search = request.args.get('search[value]')

        query = CustomerShippingAddress.query.order_by(CustomerShippingAddress.id) 
        if customer_id:
            query = query.filter(CustomerShippingAddress.customer_id == customer_id)
        if search:
            query = query.filter(
                or_(
                    CustomerShippingAddress.address_line_1.ilike(f'%{search}%'),
                    CustomerShippingAddress.address_line_2.ilike(f'%{search}%'),
                    CustomerShippingAddress.suite_apartment.ilike(f'%{search}%'),
                    CustomerShippingAddress.city.ilike(f'%{search}%'),
                    CustomerShippingAddress.state.ilike(f'%{search}%'),
                    CustomerShippingAddress.country.ilike(f'%{search}%'),
                )
            )

        start = int(request.args.get('start', 0))
        length = int(request.args.get('length', 10))
        addresses = query.offset(start).limit(length).all()

        data = []
        for index, address in enumerate(addresses,start=1):
            data.append({
                "id": index,
                "address": f"{address.city.title()},{address.state.title()},{address.country.title()}",
                "default": "Yes"  if address.is_default else "No",
                "actions": self._get_actions(address),
            })

        return jsonify({
            "draw": int(request.args.get('draw', 1)),
            "recordsTotal": CustomerShippingAddress.query.count(),
            "recordsFiltered": query.count(),
            "data": data
        })

class CustomerDocsDataTableView(MethodView):
    def _get_actions(self, obj):
        update_url = url_for('customer_bp.update_document', id=obj.id)
        delete_url = url_for('customer_bp.delete_document', id=obj.id)
        return (
            f'<div class="row"><center>'
            f'<a href="javascript:void(0)" title="Edit" data-url="{update_url}" class="update_element'
            f' text-primary mx-1"><i class="fa fa-edit"></i></a>'
            f'<label style="cursor: pointer;" data-title="{obj.name}" data-url="{delete_url}"'
            f' data-id="{obj.id}" data-table="#documents_table"  data-text="Document Deleted Successfully !!!" title="Delete" class="danger delete-btn"><i class="text-danger fa'
            ' fa-trash font-medium-3 "></i></label></center></div>'
        )
    
    def _get_attachment(self,obj):
        html_content = render_template("customer/get_attachmnets.html", attachment=obj, attachment_name=obj.attachment.split("/")[-1].title() if obj.attachment else None,)
        return html_content

    def get(self):
        customer_id = request.args.get('customer_id')
        search = request.args.get('search[value]')

        query = CustomerDocuments.query.order_by(CustomerDocuments.id) 
        if customer_id:
            query = query.filter(CustomerDocuments.customer_id == customer_id)
        if search:
            query = query.filter(
                or_(
                    CustomerDocuments.name.ilike(f'%{search}%'),
                )
            )

        start = int(request.args.get('start', 0))
        length = int(request.args.get('length', 10))
        documents = query.offset(start).limit(length).all()

        data = []
        for index, doc in enumerate(documents,start=1):
            data.append({
                "id": index,
                "name": doc.name,
                "attachment": self._get_attachment(doc),
                "actions": self._get_actions(doc),
            })

        return jsonify({
            "draw": int(request.args.get('draw', 1)),
            "recordsTotal": CustomerDocuments.query.count(),
            "recordsFiltered": query.count(),
            "data": data
        })

class CustomerDetailView(MethodView):
    def get(self, id):
        customer_obj = Customer.query.get(id)
        return render_template(
            "customer/customer_details.html",
            customer=customer_obj,
        )