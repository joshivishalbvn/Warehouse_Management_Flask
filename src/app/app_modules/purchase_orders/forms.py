from flask_wtf import FlaskForm
from flask_wtf import FlaskForm
from wtforms import BooleanField, FieldList, FormField, StringField, DecimalField, TextAreaField, SelectField, FileField, IntegerField, SelectMultipleField
from wtforms.validators import DataRequired, Optional
from flask_wtf.file import FileAllowed
from ..vendors.models import Vendor
from ..company.models import Company
from ..products.models import Product,ProductCase



class PurchaseOrderProductForm(FlaskForm):
    product_id = SelectField('Product', coerce=int, validators=[DataRequired()])
    case_size_id = SelectField('Case Size', coerce=int, validators=[DataRequired()])
    case_quantity = IntegerField('Case Quantity', validators=[DataRequired()])
    total_pieces = IntegerField('Total Pieces', default=0, validators=[Optional()])
    per_piece_price = DecimalField('Price Per Piece', places=2, default=0.0, validators=[DataRequired()])
    amount = DecimalField('Amount', places=2, default=0.0, validators=[Optional()])
    DELETE = BooleanField()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.product_id.choices = [(product.id, product.name) for product in Product.query.all()]
        self.case_size_id.choices = [(case.id,f'{case.quantity} Qty, {case.weight} Oz, {case.cubic_meter_volume} CMV') for case in ProductCase.query.all()]


class PurchaseOrderCreateForm(FlaskForm):
    company_id = SelectField('Company', coerce=int, validators=[DataRequired()])
    vendor_id = SelectField('Vendor', coerce=int, validators=[DataRequired()])
    total_price = DecimalField('Total Price', places=2, default=0.0, validators=[Optional()])
    remarks = TextAreaField('Remarks', validators=[Optional()])
    invoice = FileField('Invoice', validators=[FileAllowed(['pdf', 'jpg', 'png'], 'Images and PDFs only!'), Optional()])
    
    products = FieldList(FormField(PurchaseOrderProductForm), min_entries=0)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.vendor_id.choices = [(vendor.id, vendor.full_name) for vendor in Vendor.query.all()]
        self.vendor_id.choices.insert(0, (0, 'Select Vendor'))
        self.company_id.choices = [(company.id, company.name) for company in Company.query.all()]
        self.company_id.choices.insert(0, (0, 'Select Company'))

        # Apply 'form-control' class to all fields
        for field_name, field in self._fields.items():
            if hasattr(field.widget, 'attrs'):
                field.widget.attrs.update({'class': 'form-control'})

        


class MultiplePurchaseOrderProductForm(FlaskForm):
    products = FieldList(FormField(PurchaseOrderProductForm), min_entries=1)
    
