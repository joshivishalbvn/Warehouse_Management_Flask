import random
import string
from sqlalchemy import desc, or_
from flask.views import MethodView
from flask import jsonify,render_template, request, url_for

from app import db
from ..company.models import Company
from app.app_modules.users.models import User
from app.app_modules.users.forms import UserForm
from app.app_modules.base.base_views import BaseCreateView, BaseListView


class UserListView(BaseListView):
    
    model = User
    template_name = 'users/user_list.html' 

    def get_context_data(self,**kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["users"] = User.query.all()
        ctx["company_list"] = Company.query.order_by(Company.id) 
        return ctx

class DeleteUser(MethodView):
    
    def post(self, user_id):
        try:
            user = User.query.get_or_404(user_id)
            db.session.delete(user)
            db.session.commit()
            return jsonify({'message': 'User deleted successfully.'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': str(e)}), 500
  
class CreateUserView(BaseCreateView):

    model = User
    form_class = UserForm
    template_name = 'users/user_create.html'
    # success_url = 'user_bp.user_list'

    def post(self, **kwargs):
        form = self.form_class(request.form, **self.get_form_kwargs())
        if form.validate_on_submit():
            try:
                user = User(
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    email=form.email.data,
                    mobile=form.mobile.data,
                    role=form.role.data,
                    company_id=form.company_id.data,
                )
                password = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
                user.set_password(password)
                
                db.session.add(user)
                db.session.commit()

                return jsonify({'status': 'success', 'message': 'User created successfully!'}), 200
            except Exception as e:
                db.session.rollback()
                return jsonify({'status': 'error', 'errors': form.errors}), 400
        else:
            return jsonify({'status': 'error', 'errors': form.errors}), 400
        
class UserUpdateView(MethodView):
    def get(self, id):
        user_obj = User.query.get_or_404(id)
        form = UserForm(obj=user_obj)
        return render_template('users/user_update.html', form=form,instance=user_obj)

    def post(self, id):
        user_obj = User.query.get_or_404(id)
        form = UserForm(request.form, obj=user_obj)
        if form.validate_on_submit():
            try:
                form.populate_obj(user_obj)
                db.session.commit()
                return jsonify({'status': 'success', 'message': 'User updated successfully!'}), 200
            except Exception as e:
                db.session.rollback()
                return jsonify({'status': 'error', 'errors': form.errors}), 400
        return jsonify({'status': 'error', 'errors': form.errors}), 400
    

class UserDataTableView(MethodView):

    def _get_actions(self, obj):
        update_url = url_for('user_bp.update_user', id=obj.id)
        delete_url = url_for('user_bp.delete_user', user_id=obj.id)
        return f"""
            <span data-url='{update_url}' title='Edit' class='update_this_user' style='color:var(--primary-bg-color); cursor: pointer;'>
                <i class='fa fa-edit'></i>
            </span>
            <label data-title='{obj.first_name} {obj.last_name}' data-id='{obj.id}' title='Delete' data-url='{delete_url}' class='text-danger delete-btn text-center'>
                <i class='fa fa-trash'></i>
            </label>
        """

    def get(self):
        company_id = request.args.get('company')
        role = request.args.get('role')
        search = request.args.get('search[value]')

        query = User.query.filter(User.role != User.CUSTOMER).order_by(desc(User.id))
        if company_id:
            query = query.filter(User.company_id == company_id)
        if role:
            query = query.filter(User.role == role)
        if search:
            query = query.filter(
                or_(
                    User.first_name.ilike(f'%{search}%'),
                    User.last_name.ilike(f'%{search}%'),
                    User.email.ilike(f'%{search}%'),
                    User.mobile.ilike(f'%{search}%'),
                    User.role.ilike(f'%{search}%'),
                )
            )

        start = int(request.args.get('start', 0))
        length = int(request.args.get('length', 10))
        users = query.offset(start).limit(length).all()

        data = []
        for index, user in enumerate(users,start=1):
            data.append({
                "id": index,
                "email": user.email,
                "full_name": f"{user.first_name} {user.last_name}".title() if user.last_name else f"{user.first_name}".title(),
                "mobile": user.mobile or "-----",
                "role": user.role.title() if user.role else None,
                "actions": self._get_actions(user),
            })

        return jsonify({
            "draw": int(request.args.get('draw', 1)),
            "recordsTotal": User.query.count(),
            "recordsFiltered": query.count(),
            "data": data
        })
    
class EmployeeDataTableView(MethodView):

    def _get_actions(self, obj):
        update_url = url_for('user_bp.update_user', id=obj.id)
        delete_url = url_for('user_bp.delete_user', user_id=obj.id)
        return f"<span data-url='{update_url}' title='Edit' class='update_this_user' style='color:var(--primary-bg-color); cursor: pointer;''><i class='fa fa-edit'></i></span> <label data-title='{obj.first_name} {obj.last_name}' data-id='{obj.id}' title='Delete' data-url='{delete_url}' class='text-danger delete-btn text-center'><i class='fa fa-trash'></i></label>"

    def get(self):
        company_id = request.args.get('company')
        role = request.args.get('role')
        search = request.args.get('search[value]')

        query = User.query.filter(User.role != User.CUSTOMER).order_by(desc(User.id))
        if company_id:
            query = query.filter(User.company_id == company_id)
        if role:
            query = query.filter(User.role == role)
        if search:
            query = query.filter(
                or_(
                    User.first_name.ilike(f'%{search}%'),
                    User.last_name.ilike(f'%{search}%'),
                    User.email.ilike(f'%{search}%'),
                    User.mobile.ilike(f'%{search}%'),
                    User.role.ilike(f'%{search}%'),
                )
            )

        start = int(request.args.get('start', 0))
        length = int(request.args.get('length', 10))
        users = query.offset(start).limit(length).all()

        data = []
        for index, user in enumerate(users,start=1):
            data.append({
                "id": index,
                "email": f"{user.first_name} {user.last_name}".title() if user.last_name else f"{user.first_name}".title(),
                "name": user.email,
                "mobile": user.mobile or "-----",
                "role": user.role.title() if user.role else None,
            })

        return jsonify({
            "draw": int(request.args.get('draw', 1)),
            "recordsTotal": User.query.count(),
            "recordsFiltered": query.count(),
            "data": data
        })

class GetSalesRepresentativeAjax(MethodView):
    def get(self):
        company_id = request.args.get('company_id')
        qs = User.query.filter_by(role=User.SALES_REPRESENTATIVE,company_id=company_id)
        default_option = {
            "id": "", 
            "text": "Select Sales Representative",
        }

        user_list = [
            default_option  
        ] + [
            {
                "id": user.id,
                "text":user.get_full_name,
            }
            for user in qs.all()
        ]
        
        return jsonify({'users': user_list})