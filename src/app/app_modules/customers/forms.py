from .models import Customer
from ..users.models import User
from flask_wtf import FlaskForm
from ..company.models import Company
from flask_wtf.file import FileAllowed
from wtforms.validators import DataRequired, Optional
from wtforms import BooleanField, StringField, SelectField, FileField, IntegerField

class CustomerForm(FlaskForm):
    status                  = SelectField('Status',choices=Customer.STATUS_CHOICES,default=Customer.ACTIVE)
    type                    = SelectField('Customer Type',choices=Customer.CUSTOMER_CHOICES,validators=[DataRequired()])
    bill_to                 = StringField('Bill To Country', validators=[Optional()])
    first_name              = StringField('First Name', validators=[DataRequired()])
    last_name               = StringField('Last Name', validators=[DataRequired()])
    email                   = StringField('Email', validators=[DataRequired()])
    ship_to                 = StringField('Ship To Country', validators=[Optional()])
    sales_representative_id = SelectField('Sales Representative ID', validators=[DataRequired()])
    company_id              = SelectField('Company', coerce=int, validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(CustomerForm,self).__init__(*args, **kwargs)
        self.sales_representative_id.choices = [(user.id, user.get_full_name) for user in User.query.filter_by(role=User.SALES_REPRESENTATIVE)]
        self.sales_representative_id.choices.insert(0, (0, 'Select Sales Representative'))
        self.company_id.choices = [(company.id, company.name) for company in Company.query.all()]
        self.company_id.choices.insert(0, (0, 'Select Company'))
        self.type.choices.insert(0, (0, 'Select Type'))

class CustomerDocumentForm(FlaskForm):
    name        = StringField('Name', validators=[DataRequired()])
    attachment  = FileField('Attachment', validators=[Optional(),FileAllowed(['jpg', 'png', 'pdf'], 'Images and documents only!')])
    customer_id = IntegerField(validators=[Optional()])

class CustomerContactsForm(FlaskForm):
    name        = StringField('Name', validators=[DataRequired()])
    email       = StringField('Email', validators=[DataRequired()])
    phone       = StringField('Mobile Number', validators=[DataRequired()])
    customer_id = IntegerField(validators=[Optional()])

class CustomerAddressForm(FlaskForm):
    customer_id     = IntegerField(validators=[Optional()])
    suite_apartment = StringField('Suite/Apartment', validators=[DataRequired()])
    address_line_1  = StringField('Address Line 1', validators=[Optional()])
    address_line_2  = StringField('Address Line 2', validators=[Optional()])
    city            = StringField('City', validators=[DataRequired()])
    state           = StringField('State', validators=[DataRequired()])
    country         = StringField('Country', validators=[DataRequired()])
    zip_code        = StringField('Zip Code', validators=[DataRequired()])
    latitude        = StringField('Latitude', validators=[Optional()])
    longitude       = StringField('Longitude', validators=[Optional()])
    is_default      = BooleanField('Default Address', validators=[Optional()])

