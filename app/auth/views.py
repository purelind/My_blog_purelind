from ..models import Post, User
from . import auth
from .forms import LoginForm
from flask_login import login_user, logout_user, current_user, login_required

from flask import render_template, redirect, request, url_for, flash


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or 'main.admin')
        flash('Invalid.')
    return render_template('auth/login.html', form=form)


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed and request.endpoint[:5] != 'auth.':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_annoyous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfimed/html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))






