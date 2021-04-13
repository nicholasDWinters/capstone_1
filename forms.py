from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, PasswordField
from wtforms.validators import InputRequired, Email, Length

class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[InputRequired(message='Username is required.')])
    email = StringField('E-mail', validators=[InputRequired(message='Email is required.'), Email(message='Please enter a valid email address.')])
    password = PasswordField('Password', validators=[Length(min=6, message='Password must be longer than 6 characters.'), InputRequired(message='Please enter password.')])
    


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[InputRequired(message='Username is required.')])
    password = PasswordField('Password', validators=[Length(min=6, message='Password must be longer than 6 characters.'), InputRequired(message='Please enter password.')])