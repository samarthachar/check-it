from wtforms import StringField, SubmitField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired, Length, Email
from flask_wtf import FlaskForm


class SignUpForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email(message="Please enter a valid email address.")])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=32, message="Password must be between 8 and 32 characters.")])
    submit = SubmitField('Sign Up!')

class LogInForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(),Email(message="Please enter a valid email address.")])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')