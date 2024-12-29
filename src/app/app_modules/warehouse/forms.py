# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Optional

from app.app_modules.company.models import Company

class WarehouseForm(FlaskForm):
    name            = StringField('Name', validators=[DataRequired()])
    address_line_1  = StringField('Address Line 1', validators=[Optional()])
    address_line_2  = StringField('Address Line 2', validators=[Optional()])
    city            = StringField('City', validators=[Optional()])
    state           = StringField('State', validators=[Optional()])
    zip_code        = IntegerField('Zip Code', validators=[Optional()])
    country         = StringField('Country', validators=[Optional()])
    status          = SelectField('Status', choices=[('Active', 'Active'), ('Inactive', 'Inactive')], validators=[Optional()])
    company_id      = SelectField('Company', coerce=int, validators=[Optional()])


    def __init__(self, *args, **kwargs):
        super(WarehouseForm, self).__init__(*args, **kwargs)
        self.company_id.choices = [(company.id, company.name) for company in Company.query.all()]
        self.company_id.choices.insert(0, (0, 'Select Company'))

        
class WarehouseUpdateForm(FlaskForm):
    name            = StringField('Name', validators=[DataRequired()])
    address_line_1  = StringField('Address Line 1', validators=[Optional()])
    address_line_2  = StringField('Address Line 2', validators=[Optional()])
    city            = StringField('City', validators=[Optional()])
    state           = StringField('State', validators=[Optional()])
    zip_code        = IntegerField('Zip Code', validators=[Optional()])
    country         = StringField('Country', validators=[Optional()])
    status          = SelectField('Status', choices=[('Active', 'Active'), ('Inactive', 'Inactive')], validators=[Optional()])