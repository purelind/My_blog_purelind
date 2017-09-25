# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, DateTimeField
from flask_pagedown.fields import PageDownField
from wtforms.validators import DataRequired, Length, Email


class AdminLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])  # PasswordField类表示属性为type='password'的<input>元素
    remember_me = BooleanField('Keep me logged in')  # BooleanField 表示复选框
    submit = SubmitField('Log In')


class EditPostForm(FlaskForm):
    title = StringField('Title', validators=[Length(1, 64)])
    body = TextAreaField('Markdown')
    body_html = TextAreaField('Html')
    outline = StringField('Outline', validators=[Length(0, 64)])
    created = DateTimeField('Created')
    modified = DateTimeField('Modified')
    submit = SubmitField('Submit')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[Length(1, 128)])
    body = PageDownField("What's on your mind?")
    body_html = TextAreaField("Html")
    outline = StringField('Outline', validators=[Length(0, 64)])
    created = DateTimeField('Created')
    submit = SubmitField('Submit')
