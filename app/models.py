from . import db
from datetime import datetime
from markdown import markdown
import bleach


# class Role(db.Model):
#     __tablename__ = 'roles'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64), unique=True)
#     users = db.relationship('User', backref='role', lazy='dynamic')
#
#     def __repr__(self):
#         return '<Role %r>' % self.name


# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(64), unique=True, index=True)
#     role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
#
#     def __repr__(self):
#         return '<User %r>' % self.username


class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    outline = db.Column(db.Text)
    outline_html = db.Column(db.Text)

    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('categorys.id'))

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code', 'blockquote', 'em', 'i',
                        'strong', 'li', 'ol', 'pre', 'strong', 'ul', 'h1', 'h2', 'h3', 'p']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True)
        )

    @staticmethod
    def on_changed_outline(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code', 'blockquote', 'em', 'i',
                        'strong', 'li', 'ol', 'pre', 'strong', 'ul', 'h1', 'h2', 'h3', 'p']
        target.outline_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True)
        )


db.event.listen(Post.body, 'set', Post.on_changed_body)
db.event.listen(Post.outline, 'set', Post.on_changed_outline)


class Category(db.Model):
    __tablename__="categorys"
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(64))
    count = db.Column(db.Integer)
    posts = db.relationship("Post", backref="category")

