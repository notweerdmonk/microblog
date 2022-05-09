from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Length
from app.models import User

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),
        Length(min=0, max=32)])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)],
            render_kw={'style': 'resize: none;'})
    submit = SubmitField('Save')
    cancel = SubmitField('Cancel')

    def __init__(self, orig_username, *args, **kwargs):
        super(EditProfileForm, self).__init__()
        #super().__init__()
        self.orig_username = orig_username

    def validate_username(self, username):
        if username.data != self.orig_username:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username')

class NewPostForm(FlaskForm):
    post_body = TextAreaField('New post', validators=[Length(min=0, max=140)],
            render_kw={'style': 'resize: none;'})
    post = SubmitField('Post')

class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')
