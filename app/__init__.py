from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config
from flask_admin import Admin

bootstrap = Bootstrap()
db = SQLAlchemy()

# LoginManager对象session_protection属性可以设为None,'basic',
# 'strong',提供不同的安全等级防止用户会话在遭到篡改
login_manager = LoginManager()
login_manager.session_protection = 'strong'  # Flask-Login记录客户端IP地址和浏览器用户代理信息
login_manager.login_view = 'adminauth.login'   # login_view属性设置登录页面端点？？？

from .models import User, Post
blog_admin = Admin()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)  # 初始化Flask-Login
    blog_admin.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .adminauth import adminauth as adminauth_blueprint
    app.register_blueprint(adminauth_blueprint, url_prefix='/adminauth')


    return app

