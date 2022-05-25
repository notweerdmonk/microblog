from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, PasswordField,\
        EmailField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError,\
        Length
from app.models import User

class LoginForm(FlaskForm):
    username = StringField(
            'Username', validators=[DataRequired(), Length(min=0, max=32)])
    password = PasswordField(
            'Password', validators=[DataRequired(), Length(min=0, max=32)])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField(
            'Username', validators=[DataRequired(), Length(min=0, max=32)])
    email = EmailField(
            'Email', validators=[DataRequired(), Email(), Length(min=0, max=64)])
    password = PasswordField(
            'Password', validators=[DataRequired(), Length(min=6)])
    password_verify = PasswordField(
            'Verify Password',
            validators=[DataRequired(), EqualTo('password'), Length(min=6)])
    submit = SubmitField('Sign Up')

    '''
    methods matching pattern validate_<field_name> are considered custom
    validators and are invoked alongwith stock validators
    '''
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username exists.')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email is not None:
            raise ValidationError('Email already registered.')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    repeat_password = PasswordField('Repeat Password',
            validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
