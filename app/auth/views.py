from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, logout_user, login_user
from . import auth
from .forms import LoginForm
from ..models import User



@auth.route('/admin', methods=['GET', 'POST'])
def admin():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('auth.admin_home'))
        flash('Ops, permission denied.')
    return render_template('auth/admin_login.html', form=form)


@auth.route('/admin_home')
def admin_home():
    return render_template('auth/admin_home.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))