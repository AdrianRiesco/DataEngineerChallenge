# Import libraries
from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, RadioField, SubmitField, validators
from wtforms.validators import DataRequired, InputRequired, EqualTo, Email, Length, Regexp
from flask_wtf.file import FileField, FileAllowed, FileRequired

# Class for the login form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    send = SubmitField('Log In')

# Class for the signin form
class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username (will be used for log in)', validators=[DataRequired(),
        Length(min=3, max=30, message='Username must have between 3 and 30 numbers and/or letters, and start with a letter.'),
        Regexp('^[A-Za-z]+[0-9A-Za-z]*$', message='Username must have between 3 and 30 numbers and/or letters, and start with a letter.')])
    email = StringField('Email address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password  = PasswordField('Repeat password')
    send = SubmitField('Register')

class UploadForm(FlaskForm):
    file = FileField('Choose an image', validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png'], 'Wrong file format!')])
    visibility = RadioField('Visibility', choices=[('public','Public'),('private','Private')], default='public')
    send = SubmitField('Upload')

class DeleteForm(FlaskForm):
    filename = StringField('Filename', validators=[DataRequired()])
    visibility = StringField('Visibility', validators=[DataRequired()])
    send = SubmitField('Remove')