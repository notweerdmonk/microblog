from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, BooleanField
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from wtforms.validators import Length
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
            'Email', validators=[DataRequired(), Email(), Length(min=0, max=32)])
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

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),
        Length(min=0, max=32)])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Save')
    cancel = SubmitField('Cancel')
