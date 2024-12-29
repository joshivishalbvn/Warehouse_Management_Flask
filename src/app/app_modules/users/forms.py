from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, Email, Length, Optional
from app.app_modules.users.models import User
from ..company.models import Company

class UserForm(FlaskForm):
    first_name  = StringField('First Name', validators=[Optional(), Length(max=50)])
    last_name   = StringField('Last Name', validators=[Optional(), Length(max=50)])
    email       = StringField('Email', validators=[DataRequired(), Email(), Length(max=255)])
    mobile      = StringField('Mobile', validators=[Optional(), Length(max=15)])
    role        = SelectField('Role', choices=User.USER_ROLE, validators=[Optional()])
    company_id  = SelectField('Company', coerce=int, validators=[Optional()])

    def __init__(self, *args, **kwargs):
        self.product_id = kwargs.pop('product_id', None)
        super(UserForm, self).__init__(*args, **kwargs)
        self.company_id.choices = [(company.id, company.name) for company in Company.query.all()]
        self.company_id.choices.insert(0, (0, 'Select Company'))


