from flask_wtf import FlaskForm
from wtforms import IntegerField, DateField, DecimalField,SelectField, ValidationError
from wtforms.validators import DataRequired, Optional
from ..vendors.models import Vendor
from ..warehouse.models import Warehouse
from ..zones.models import Zone
from ..products.models import ProductCase

class StockCreateForm(FlaskForm):
    modified_by_id   = IntegerField('User', default=0, validators=[Optional()])
    warehouse_id     = SelectField('Warehouse', coerce=int, validators=[Optional()])
    zone_id          = SelectField('Zone', coerce=int, validators=[Optional()])
    company_id       = IntegerField('Company', default=0, validators=[Optional()])
    vendor_id        = SelectField('Vendor', coerce=int, validators=[Optional()])
    product_case_id  = SelectField('ProductCase', coerce=int, validators=[Optional()])
    no_of_case       = IntegerField('Number of Cases', default=0, validators=[DataRequired()])
    affected_stock   = IntegerField('Affected Stock', default=0, validators=[DataRequired()])
    per_piece_price  = IntegerField('Price Per Piece', default=0, validators=[DataRequired()])
    total_amount     = DecimalField('Total Amount', places=2, default=0, validators=[DataRequired()])
    manufacture_date = DateField('Manufacture Date', format='%Y-%m-%d', validators=[Optional()])
    expiry_date      = DateField('Expiry Date', format='%Y-%m-%d', validators=[Optional()])

    def __init__(self, *args, **kwargs):
        self.product_id = kwargs.pop('product_id', None)
        self.company_id = kwargs.pop('company_id', None)
        company_id = int(self.company_id)
        product_id = int(self.product_id)

        super(StockCreateForm, self).__init__(*args, **kwargs)
        self.affected_stock.render_kw = {'disabled': True}
        self.total_amount.render_kw = {'disabled': True}
        
        self.vendor_id.choices = [(vendor.id, vendor.full_name) for vendor in Vendor.query.all()]
        self.warehouse_id.choices = [(warehouse.id, warehouse.name) for warehouse in Warehouse.query.all()]
        self.zone_id.choices = [(zone.id, zone.name) for zone in  Zone.query.all()]
        self.product_case_id.choices = [(case.id, f'{case.quantity} Qty, {case.weight} Oz, {case.cubic_meter_volume} CMV') for case in  ProductCase.query.all()]

        if company_id:
            self.vendor_id.choices = [(vendor.id, vendor.full_name) for vendor in Vendor.query.filter_by(company_id=company_id)]
            self.vendor_id.choices.insert(0, (0, 'Select Vendor'))
            self.warehouse_id.choices = [(warehouse.id, warehouse.name) for warehouse in Warehouse.query.filter_by(company_id=company_id).all()]
            self.warehouse_id.choices.insert(0, (0, 'Select Warehouse'))

            self.zone_id.choices = [(zone.id, zone.name) for zone in  Zone.query.filter(Zone.warehouse.has(company_id=company_id)).order_by(Zone.id).all()]
            self.zone_id.choices.insert(0, (0, 'Select Zone'))

            if product_id:
                self.product_case_id.choices = [(case.id, f'{case.quantity} Qty, {case.weight} Oz, {case.cubic_meter_volume} CMV') for case in  ProductCase.query.filter_by(product_id=product_id).all()]
                self.product_case_id.choices.insert(0, (0, 'Select Case Size'))
