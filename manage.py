#!/usr/bin/env python3
import os
from app import create_app, db
from app.models import User, Post, Category
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('BLOG_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    """注册了程序,数据库实例,以及模型,使得这些对象可直接导入shell"""
    return dict(app=app, db=db, User=User, Post=Post, Category=Category)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)  # Flask-Migrate提供一个MigrateCommand类, 用于导出数据库迁移命令


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()
