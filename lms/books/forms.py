from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,SelectField
from wtforms.fields.core import IntegerField
from wtforms.fields.simple import MultipleFileField, TextAreaField   
from wtforms.validators import DataRequired,Email,EqualTo, URL
from wtforms import ValidationError
from flask_wtf.file import FileField,FileAllowed

from flask_login import current_user
from lms.models import User


class NewBookForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired('Data required')])
    authors=StringField('Authors', validators=[DataRequired('Data required')])
    url=StringField("Please enter the url of image of book thumbnail",validators=[DataRequired('Data required'),URL('Should be a url')])
    isbn=StringField('ISBN',validators=[DataRequired('Data required')])
    genre=StringField('Genre',validators=[DataRequired('Data required')])
    copies=IntegerField('Number of Copies',validators=[DataRequired('Data required')])
    year=IntegerField('Year of',validators=[DataRequired('Data required')])
    shelf_id=IntegerField('ID of the shelf in which it is stored.',validators=[DataRequired('Data required')])
    submitBook=SubmitField('Add book')

class RatingForm(FlaskForm):
    isbn=StringField('ISBN',validators=[DataRequired('Data required')])
    rating=SelectField('Rating out of 5',choices=[i for i in range(6)],coerce=int,validators=[DataRequired('Rating is required')])
    review=TextAreaField('Review of the book')
    submitRating=SubmitField('Submit Review')

class changeShelf(FlaskForm):
    isbn=StringField('ISBN',validators=[DataRequired('Data required')])
    shelfid=IntegerField('SHELF ID',validators=[DataRequired('Please enter the shelf id.')])
    changeShelfSubmit=SubmitField('Change Shelf')

class newShelf(FlaskForm):
    shelfid=IntegerField('SHELF ID',validators=[DataRequired('Please enter the shelf id.')])
    capacity=IntegerField('Capacity',validators=[DataRequired('Please enter the capacity.')])
    newShelfSubmit=SubmitField('Create new shelf.')