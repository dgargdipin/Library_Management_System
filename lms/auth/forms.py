from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,SelectField
from wtforms.fields.simple import MultipleFileField, TextAreaField   
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField,FileAllowed

from flask_login import current_user
from lms.models import User

class LoginForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired('Data required'),Email('email required')])
    password=PasswordField('Password',validators=[DataRequired('Data required')])
    submit=SubmitField('Login')

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired('Data required')])
    about = TextAreaField('About you', validators=[DataRequired('Data required')])
    email=StringField('Email',validators=[DataRequired('Data required'),Email('email required')])
    password=PasswordField('Password',validators=[DataRequired('Data required'),
    EqualTo('pass_confirm',message="Passwords must match!")])
    pass_confirm=PasswordField('Confirm Password',validators=[DataRequired('Data required')])
    submit=SubmitField('Register')
    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already')
    

class UpdateUserForm(FlaskForm):
    email=StringField('Email',validators=[Email('email required')])
    password=StringField('Password')
    submit=SubmitField('Update')
    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already')
    