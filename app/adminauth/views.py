
from ..models import Post, User
from . import adminauth
from .forms import LoginForm
from flask_login import login_user

from flask import render_template, redirect, request, url_for, flash

@adminauth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid.')
    return render_template('adminauth/login.html', form=form)






