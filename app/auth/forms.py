from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])  # PasswordField类表示属性为type='password'的<input>元素
    remember_me = BooleanField('Keep me logged in')  # BooleanField 表示复选框
    submit = SubmitField('Log In')
