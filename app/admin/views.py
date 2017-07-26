from . import admin
from .. import db
from ..models import Post
from .forms import EditPostForm
from flask import render_template, redirect, url_for, abort, flash, request, current_app,make_response
from flask_sqlalchemy import get_debug_queries
from flask_login import login_required, logout_user, login_user, current_user





@admin.route('/home', methods=['GET', 'POST'])
# @login_required
def home():
    posts = Post.query.order_by(Post.created.desc()).all()
    return render_template('admin/home.html', posts=posts)


@admin.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    form = EditPostForm()
    if form.validate_on_submit():
        post = Post()
    return render_template('admin/postlist.html')

@admin.route('/edit/<int:id>', methods=['GET', 'POST'])
# @login_required
def edit(id):
    post = Post.query.get_or_404(id)
    # if current_user != 'admin':
    #     abort(403)
    form = EditPostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        post.body_html = form.body_html.data
        post.outline = form.outline.data
        post.created = form.created.data
        post.modified = form.modified.data
        db.session.add(post)
        flash('The post has been updated')
        return redirect(url_for('main.post', id=post.id))
    form.title.data = post.title
    form.body.data = post.body
    form.body_html = post.body_html
    form.outline.data = post.outline
    form.created.data = post.created
    form.modified.data = post.modified
    return render_template('admin/edit_post.html', form=form)





