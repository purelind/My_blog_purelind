from flask import render_template
from ..models import Post, User, db
from . import main


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


from flask_admin.contrib.sqla import ModelView
from .. import blog_admin
class MyBlogModelView(ModelView):
    can_delete = False
    page_size = 10



blog_admin.add_view(MyBlogModelView(Post, db.session))
blog_admin.add_view(MyBlogModelView(User, db.session))