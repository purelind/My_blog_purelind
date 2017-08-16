from . import db
from datetime import datetime
from markdown import markdown
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import bleach
from .import login_manager


class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80


#  class User 继承自 db.Model 时, SQLAlchemy 与 数据库的连接通过就已经自动的 Ready 了.
class User(UserMixin, db.Model):  # UserMixin类: is_authenticated(), is_active(), is_annoymous(), get_id()
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    last_seen = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    avatar_hash = db.Column(db.String(32))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def ping(self):  # 刷新用户的最后访问时间
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def __repr__(self):
        return "<Model User '{}'>".format(self.username)

@login_manager.user_loader
def load_user(user_id):
    """Flask-Login 要求程序实现一个回调函数,使用指定的标识符加载用户 ？？？"""
    return User.query.get(int(user_id))

posts_tags = db.Table('posts_tags',
                      db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
                      db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')))


class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    body = db.Column(db.Text)
    body_md = db.Column(db.Text)
    body_html = db.Column(db.Text)
    outline = db.Column(db.Text)

    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    modified = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    """db.ForeignKey()的参数'catefory.id'表明，这列的值是category表中行的id值
        文章对分类：一对多关系,将一个记录和一组记录联系在一起;
        实现这种关系时,需要在‘多’一侧加入一个外键,指向‘一’一侧联接的记录"""
    category_id = db.Column(db.Integer, db.ForeignKey('categorys.id'))

    tags = db.relationship('Tag',
                           secondary=posts_tags,
                           backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, title):
        self.title = title

    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed, randint
        import forgery_py

        seed()
        for i in range(count):
            post = Post(title=forgery_py.lorem_ipsum.sentence(),
                        body=forgery_py.lorem_ipsum.sentences(randint(10,20)),
                        body_html=forgery_py.lorem_ipsum.sentences(randint(10,30)),
                        outline=forgery_py.lorem_ipsum.sentences(randint(5,10)),
                        created=forgery_py.date.date(True),
                        modified=forgery_py.date.date(True))
            db.session.add(post)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code', 'blockquote', 'em', 'i',
                        'strong', 'li', 'ol', 'pre', 'strong', 'ul', 'h1', 'h2', 'h3', 'p']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True)
        )

    def __repr__(self):
        return "<Model Post '{}'>".format(self.title)

db.event.listen(Post.body, 'set', Post.on_changed_body)


class Category(db.Model):
    __tablename__ = "categorys"
    id = db.Column(db.Integer, primary_key=True)
    categoryname = db.Column(db.String(64))
    count = db.Column(db.Integer)
    posts = db.relationship("Post", backref="category")  # backref参数向Post模型中添加一个category属性,从而定义反向关系

    def __repr__(self):
        return "<Model Category '{}'>".format(self.categoryname)


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    tagname = db.Column(db.String(255))

    def __init__(self, tagname):
        self.tagname = tagname

    def __repr__(self):
        return "<Model Tag '{}'>".format(self.tagname)
