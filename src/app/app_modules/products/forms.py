from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField,SelectField, SubmitField
from wtforms.validators import DataRequired , Optional , ValidationError , InputRequired
from ..company.models import Company
from flask_wtf.file import FileField
from .models import Barcode, Product


def non_zero_validator(form, field):
    if field.data <= 0:
        raise ValidationError(f"{field.label.text} must be greater than zero.")

class ProductCaseForm(FlaskForm):
    weight = FloatField('Weight', default=0, validators=[non_zero_validator])
    quantity = IntegerField('Quantity', default=0, validators=[non_zero_validator])
    cubic_meter_volume = FloatField('Cubic Meter Volume', default=0, validators=[non_zero_validator])
    product_id = IntegerField(validators=[Optional()])

class ProductImageForm(FlaskForm):
    image_url = FileField()

class ProductForm(FlaskForm):
    name            = StringField('Name', validators=[DataRequired()])
    code            = StringField('Code')
    status          = SelectField('Status', choices=[('Active', 'Active'), ('Inactive', 'Inactive')], validators=[Optional()])
    product_image   = FileField('Product Image')
    company_id      = SelectField('Company', coerce=int, validators=[Optional()])

    
    def __init__(self, *args, **kwargs):
        self.product_id = kwargs.pop('product_id', None)
        super(ProductForm, self).__init__(*args, **kwargs)
        self.company_id.choices = [(company.id, company.name) for company in Company.query.all()]
        self.company_id.choices.insert(0, (0, 'Select Company'))

    def validate_code(self, field):
        if self.product_id:
            # Check if the code exists for any product except the current one
            existing_product = Product.query.filter_by(code=field.data).filter(Product.id != self.product_id).first()
            if existing_product:
                raise ValidationError("A product with this code already exists.")
        else:
            # If creating a new product, simply check for existence
            if Product.query.filter_by(code=field.data).first():
                raise ValidationError("A product with this code already exists.")

def dupicate_barcode_number(form,field):
    existing_barcode = Barcode.query.filter_by(number=str(field.data)).first()
    if existing_barcode:
        raise ValidationError(f"{field.label.text} barcode number already in use")
    
class BarcodeCreateForm(FlaskForm):
    number = IntegerField('Number', validators=[DataRequired(),dupicate_barcode_number])
    product_id = IntegerField(validators=[Optional()])


class ImportProductCSVForm(FlaskForm):
    csv_file = FileField(
        'CSV File',
        validators=[Optional()],
        render_kw={"accept": ".xlsx, .xls", "class": "form-control", "placeholder": "Upload Excel file"}
    )
    submit      = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(ImportProductCSVForm, self).__init__(*args, **kwargs)

    def validate_csv_file(self, field):
        if not field.data.filename.endswith(".xlsx"):
            raise ValidationError("Only Excel files are accepted.")
        
class BarcodeCreateFromCSVForm(FlaskForm):
    product_id = SelectField('Product', coerce=int, validators=[DataRequired()])
    number = StringField('Number', validators=[DataRequired()])