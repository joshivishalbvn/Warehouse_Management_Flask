from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from app.app_modules.users.models import User
from wtforms.validators import DataRequired, Email, Optional
from wtforms import StringField, EmailField, FileField, SelectField, ValidationError

class CompanyForm(FlaskForm):
    name   = StringField('Company Name', validators=[DataRequired()])
    email  = EmailField('Email', validators=[DataRequired(), Email()])
    phone  = StringField('Phone Number', validators=[Optional()])
    logo   = FileField('Company Logo', validators=[Optional(),FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    status = SelectField('Status', choices=[('Active', 'Active'),('Inactive', 'Inactive')], validators=[DataRequired()])

    def validate_email(self, field):
        existing_user = User.query.filter_by(email=field.data).first()
        if existing_user:
            raise ValidationError('Email already in use.')

class CompanyUpdateForm(FlaskForm):
    name   = StringField('Company Name', validators=[Optional()])
    email  = EmailField('Email', validators=[Optional(), Email()])
    phone  = StringField('Phone Number', validators=[Optional()])
    logo   = FileField('Company Logo', validators=[Optional(),FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    status = SelectField('Status', choices=[('Active', 'Active'),('Inactive', 'Inactive')], validators=[Optional()])