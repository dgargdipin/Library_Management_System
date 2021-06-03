from flask_wtf import FlaskForm

from wtforms import StringField,PasswordField,SubmitField,SelectField
from wtforms.fields.core import IntegerField
from wtforms.fields.simple import MultipleFileField, TextAreaField   
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField,FileAllowed

from flask_login import current_user
from lms.models import User




class addFriendForm(FlaskForm):
    email= StringField('email', validators=[DataRequired('Data required'),Email('Email Required')])
    submit=SubmitField('Add friend')
