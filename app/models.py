# -*- coding: utf-8 -*-
import hashlib
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

import bleach
from flask import current_app, request, url_for
from markdown import markdown
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app.exceptions import ValidationError
from . import db, login_manager


class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.FOLLOW |
                     Permission.COMMENT |
                     Permission.WRITE_ARTICLES, True),
            'Moderator': (Permission.FOLLOW |
                          Permission.COMMENT |
                          Permission.WRITE_ARTICLES |
                          Permission.MODERATE_COMMENTS, False),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return "<Model Role '{}'>".format(self.name)


#  class User 继承自 db.Model 时, SQLAlchemy 与 数据库的连接通过就已经自动的 Ready 了.
class User(UserMixin, db.Model):  # UserMixin类: is_authenticated(), is_active(), is_annoymous(), get_id()
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    last_seen = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    avatar_hash = db.Column(db.String(32))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['BLOG_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    @property
    def password(self):  # 试图读取password属性的值,返回错误,因为生成散列值后无法还原密码
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def ping(self):  # 刷新用户的最后访问时间
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'],
                       expires_in=expiration)
        return s.dumps({'id': self.id}).decode('ascii')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.load(token)
        except:
            return None
        return User.query.get(data['id'])

    def __repr__(self):
        return "<Model User '{}'>".format(self.username)


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser


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
    title = db.Column(db.String(128))
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    outline = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    modified = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    """db.ForeignKey()的参数'catefory.id'表明，这列的值是category表中行的id值
        文章对分类：一对多关系,将一个记录和一组记录联系在一起;
        实现这种关系时,需要在‘多’一侧加入一个外键,指向‘一’一侧noew联接的记录"""
    category_id = db.Column(db.Integer, db.ForeignKey('categorys.id'))

    tags = db.relationship('Tag',
                           secondary=posts_tags,
                           backref=db.backref('posts', lazy='dynamic'))

    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed, randint
        import forgery_py

        seed()
        user_count = User.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, user_count - 1)).first()
            post = Post(title=forgery_py.lorem_ipsum.sentence(),
                        body=forgery_py.lorem_ipsum.sentences(randint(10, 20)),
                        body_html=forgery_py.lorem_ipsum.sentences(randint(10, 30)),
                        outline=forgery_py.lorem_ipsum.sentences(randint(5, 10)),
                        created=forgery_py.date.date(True),
                        modified=forgery_py.date.date(True),
                        author=u)
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
            tags=allowed_tags, strip=True))

    def to_json(self):
        json_post = {
            'url': url_for('api.get_post', id=self.id, _external=True),
            'body': self.body,
            'body_md': self.body_md,
            'body_html': self.body_html,
            'created': self.created,
            'author': url_for('api.get_user', id=self.author_id,
                              _external=True)
        }
        return json_post

    @staticmethod
    def from_json(json_post):
        body = json_post.get('body')
        if body is None or body == '':
            raise ValidationError('post does not have a body')
        return Post(body=body)

db.event.listen(Post.body, 'set', Post.on_changed_body)


class Category(db.Model):
    __tablename__ = "categorys"
    id = db.Column(db.Integer, primary_key=True)
    categoryname = db.Column(db.String(64))
    count = db.Column(db.Integer)
    # backref参数向Post模型中添加一个category属性,从而定义反向关系
    posts = db.relationship("Post", backref="category")

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
