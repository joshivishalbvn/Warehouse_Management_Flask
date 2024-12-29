from .models import Vendor
from flask_wtf import FlaskForm
from ..company.models import Company
from wtforms.validators import DataRequired, Optional, Email
from wtforms import StringField, IntegerField, SelectField, EmailField, URLField

class VendorForm(FlaskForm):
    email          = EmailField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Enter email address"})
    phone          = StringField('Phone', validators=[Optional()], render_kw={"placeholder": "Enter phone number"})
    full_name      = StringField('Full Name', validators=[Optional()], render_kw={"placeholder": "Enter full name"})
    website        = URLField('Website', validators=[Optional()], render_kw={"placeholder": "Enter website URL"})
    address_line_1 = StringField('Address Line 1', validators=[Optional()], render_kw={"placeholder": "Enter address line 1"})
    address_line_2 = StringField('Address Line 2', validators=[Optional()], render_kw={"placeholder": "Enter address line 2"})
    state          = StringField('State', validators=[DataRequired()], render_kw={"placeholder": "Enter state"})
    city           = StringField('City', validators=[DataRequired()], render_kw={"placeholder": "Enter city"})
    zip_code       = IntegerField('Zip Code', validators=[Optional()], render_kw={"placeholder": "Enter zip code"})
    country        = StringField('Country', validators=[Optional()], render_kw={"placeholder": "Enter country"})
    status         = SelectField('Status', choices=Vendor.VENDOR_STATUS, default=Vendor.ACTIVE)
    company_id     = SelectField('Company', coerce=int, validators=[Optional()])

    def __init__(self, *args, **kwargs):
        super(VendorForm, self).__init__(*args, **kwargs)
        self.company_id.choices = [(company.id, company.name) for company in Company.query.all()]
        self.company_id.choices.insert(0, (0, 'Select Company'))
        self.status.choices.insert(0, (0, 'Select Status'))