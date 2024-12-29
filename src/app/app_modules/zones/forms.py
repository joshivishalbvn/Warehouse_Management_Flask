from flask_wtf import FlaskForm
from wtforms import StringField, SelectField , IntegerField, ValidationError
from wtforms.validators import DataRequired,Length, Optional
from .models import Zone

class ZoneForm(FlaskForm):
    name         = StringField('Name', validators=[DataRequired(), Length(max=50)])
    status       = SelectField('Status', choices=Zone.STATUS_CHOICES, validators=[Optional()])
    warehouse_id = IntegerField(validators=[Optional()])

    def __init__(self, *args, **kwargs):
        self.zone_id = kwargs.pop('zone_id', None)
        super(ZoneForm, self).__init__(*args, **kwargs)

    def validate_name(self, field):
        if field.data and self.warehouse_id.data is not None:
            if self.zone_id:
                existing_zone = Zone.query.filter_by(name=field.data, warehouse_id=self.warehouse_id.data).filter(Zone.id != self.zone_id).first()
                if existing_zone:
                    raise ValidationError("Zone with this name already exists in the selected warehouse.")
            else:
                existing_zone = Zone.query.filter_by(name=field.data, warehouse_id=self.warehouse_id.data).first()
                if existing_zone:
                    raise ValidationError("Zone with this name already exists in the selected warehouse.")

