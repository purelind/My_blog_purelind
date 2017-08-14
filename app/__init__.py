from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()  # db 是 class SQLAlchemy 的实例化对象, 包含了 SQLAlchemy 对数据库操作的支持类集.

# LoginManager对象session_protection属性可以设为None,'basic',
# 'strong',提供不同的安全等级防止用户会话在遭到篡改
login_manager = LoginManager()
login_manager.session_protection = 'strong'  # Flask-Login记录客户端IP地址和浏览器用户代理信息
login_manager.login_view = 'auth.login'   # login_view属性设置登录页面端点？？？


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)  # 初始化Flask-Login

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app

