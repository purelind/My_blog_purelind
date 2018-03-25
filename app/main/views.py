# -*- coding: utf-8 -*-
from flask import current_app, render_template, redirect, request, url_for, flash
from flask_login import login_required

from . import main
from .forms import EditPostForm, PostForm

from .. import db
from ..models import Post


@main.route('/', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    '''其中 Post.query 返回的是 flask_sqlalchemy.BaseQuery object
       flask_sqlalchemy.BaseQuery object 拥有对数据库操作的所有抽像方法'''
    query = Post.query
    pagination = query.order_by(Post.created.desc()).paginate(
        page, per_page=current_app.config['BLOG_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('index.html', posts=posts, pagination=pagination)


@main.route('/post/<int:id>', methods=['GET'])
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html', post=post)


@main.route('/about', methods=['GET'])
def about_site():
    return render_template('about.html')


@main.route('/projects', methods=['GET'])
def projects():
    return render_template('projects.html')


@main.route('/archives', methods=['GET'])
def archives():
    posts = Post.query.order_by(Post.created.desc()).all()
    return render_template('archives.html', posts=posts)


@main.route('/blogroll', methods=['GET'])
def blogroll():
    return render_template('blogroll.html')


@main.route('/resume', methods=['GET'])
def resume():
    return render_template('resume.html')


@main.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    posts = Post.query.order_by(Post.created.desc()).all()
    return render_template('admin.html', posts=posts)


@main.route('/admin/postlist', methods=['GET', 'POST'])
@login_required
def postlist():
    form = EditPostForm()
    if form.validate_on_submit():
        post = Post()
    return render_template('postlist.html')


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
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
    form.body_html.data = post.body_html
    form.outline.data = post.outline
    form.created.data = post.created
    form.modified.data = post.modified
    return render_template('edit_post.html', form=form, post=post)


@main.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = PostForm()
    post = Post()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        post.body_html = form.body_html.data
        post.outline = form.outline.data
        post.created = form.created.data
        db.session.add(post)
        return redirect(url_for('main.admin'))
    try:
        db.session.commit()
    except ImportError:
        db.session.rollback
    return render_template('create_post.html', form=form)



