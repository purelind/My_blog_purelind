from flask import render_template, render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required

from .forms import AdminLoginForm, EditPostForm
from ..models import Post, User

from . import main

from .. import db
from ..models import Post
from .forms import EditPostForm, PostForm
from flask_sqlalchemy import get_debug_queries





@main.route('/', methods=['GET', 'POST'])
def index():
    posts = Post.query.order_by(Post.created.desc()).all()
    return render_template('index.html', posts=posts)


@main.route('/post/<int:index>', methods=['GET'])
def post(index):
    post = Post.query.get_or_404(index)
    return render_template('post.html', post=post)


@main.route('/about', methods=['GET'])
def about_site():
    return render_template('about.html')


@main.route('/admin', methods=['GET', 'POST'])
def admin():
    posts = Post.query.order_by(Post.created.desc()).all()
    return render_template('admin.html', posts=posts)








# @main.route('/home', methods=['GET', 'POST'])
# # @login_required
# def home():
#     posts = Post.query.order_by(Post.created.desc()).all()
#     return render_template('home.html', posts=posts)


@main.route('/admin/postlist', methods=['GET', 'POST'])
@login_required
def postlist():
    form = EditPostForm()
    if form.validate_on_submit():
        post = Post()
    return render_template('postlist.html')

@main.route('/edit/<int:id>', methods=['GET', 'POST'])
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
        return redirect(url_for('main.admin'))
    form.title.data = post.title
    form.body.data = post.body
    form.body_html = post.body_html
    form.outline.data = post.outline
    form.created.data = post.created
    form.modified.data = post.modified
    return render_template('edit_post.html', form=form, post=post)

@main.route('/create', methods=['GET', 'POST'])
def create():
    form = PostForm()
    post = Post()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        post.outline = form.outline.data
        post.created = form.created.data
        db.session.add(post)
        return redirect(url_for('main.admin'))
    try:
        db.session.commit()
    except ImportError:
        db.session.rollback
    return render_template('create_post.html', form=form)




