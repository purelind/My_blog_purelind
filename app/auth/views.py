from ..models import User
from . import auth
from .forms import LoginForm
from flask_login import login_user, logout_user, login_required
from flask import render_template, redirect, url_for, flash
from config import Config
from ..email import send_email


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            if Config.BLOG_ADMIN:
                send_email(Config.BLOG_ADMIN, 'Admin Login Alert', 'mail/admin_login_alert', user=user)
            return redirect('admin')
        flash('Invalid.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))






