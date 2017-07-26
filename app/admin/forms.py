from flask_wtf import Form, FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, DateTimeField
from wtforms.validators import DataRequired, Length, Email


class EditPostForm(FlaskForm):
    title = StringField('Title', validators=[Length(1, 64)])
    body = TextAreaField('Markdown')
    body_html = TextAreaField('Html')
    outline = StringField('Outline', validators=[Length(0, 64)])
    created = DateTimeField('Created')
    modified = DateTimeField('Modified')
    submit = SubmitField('Submit')

