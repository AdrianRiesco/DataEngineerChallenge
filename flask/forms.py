# Import libraries
from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, RadioField, SubmitField, validators
from wtforms.validators import DataRequired, InputRequired, EqualTo, Email
from flask_wtf.file import FileField, FileAllowed, FileRequired

# Class for the login form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    send = SubmitField('Log In')

# Class for the signin form
class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password  = PasswordField('Repeat password')
    send = SubmitField('Register')

class UploadForm(FlaskForm):
    file = FileField('Choose an image', validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png'], 'Wrong file format!')])
    visibility = RadioField('Visibility', choices=[('public','Public'),('private','Private')], default='public')
    send = SubmitField('Upload')