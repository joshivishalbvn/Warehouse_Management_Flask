from flask import flash, jsonify, redirect, render_template, request, url_for
from flask.views import MethodView
from app import db

class BaseListView(MethodView):

    model = None
    template_name = None  

    def get_context_data(self,**kwargs):

        """
        Provides additional context data for the view.
        """

        context = {}
        context.update(**kwargs)
        return context
    
    def get_queryset(self):

        """
        Override this method to return a queryset of resources.
        """

        return self.model.query.all() if self.model else None

    def get(self,**kwargs):

        """
        Fetch all resources and render a template or return JSON.
        """

        resources = self.get_queryset()
        context = self.get_context_data(resources=resources, **kwargs)
        
        if self.template_name:
            return render_template(self.template_name, **context)
        else:
            data = [self.serialize(resource) for resource in resources]
            return jsonify(data)

class BaseCreateView(MethodView):

    """
    A base class for creating resources, similar to Django's CreateView.
    """
    
    model = None
    form_class = None
    template_name = None
    success_url = None
    message = None
    error_message = "There was an error processing your request."
    
    def get_context_data(self, form=None, **kwargs):

        """
        Provides additional context data for the view.
        """

        context = {
            'form': form
        }
        context.update(**kwargs)
        return context
    
    def get_form_kwargs(self,**kwargs):
        """
        Returns additional keyword arguments for form initialization.
        """
        # Example: returning user-specific or context-specific data
        data = {}
        data.update(**kwargs)
        return data

    def get(self, **kwargs):

        """
        Render a template with a form for creating a new resource.
        """

        form = self.form_class(**self.get_form_kwargs())
        context = self.get_context_data(form=form, **kwargs)
        if self.template_name:
            return render_template(self.template_name, **context)
        return jsonify({'message': 'GET request received'})

    def post(self, **kwargs):

        """
        Process the form data and create a new resource.
        """

        form = self.form_class(request.form, **self.get_form_kwargs())
        if form.validate_on_submit():
            try:
                # Create and save the new resource
                instance_data = {k: v for k, v in form.data.items() if k != 'csrf_token'}
                instance = self.model(**instance_data)
                db.session.add(instance)
                db.session.commit()
                flash('Resource created successfully!', 'success')

                if self.success_url:
                    return redirect(url_for(self.success_url))
                else:
                     return jsonify({'status': 'success', 'message': self.message}), 200
            except Exception as e:
                db.session.rollback()
                flash(str(e), 'error')
                return jsonify({'status': 'error', 'errors': form.errors}), 400
        else:
            return jsonify({'status': 'error', 'errors': form.errors}), 400

    def render_form_with_errors(self, form):

        """
        Render the form with validation errors.
        """

        context = self.get_context_data(form=form)
        if self.template_name:
            return render_template(self.template_name, **context)
        return jsonify({'message': 'Form validation failed', 'errors': form.errors})