## My Blog with Flask

使用Flask框架搭建的个人博客项目：尽量的保持前端页面的简洁与后端功能的精简。

#### 特性

* 极简的页面
* 更多特性待更新

查看特性详细说明 blog features。

#### 安装

* 环境要求：Python 3.4+

#### 使用

1. 安装python第三方库，推荐使用virtualenv，建立项目独立的python运行环境。Debian环境下步骤：

  ```
  # 安装virtualenv
  $ [sudo] pip install virtualenv
  ```

2. 建立名为venv的独立环境并安装项目所需第三方库：

  ```
  # 项目根目录下，manage.py所在目录
  $ virtualenv -p /usr/bin/python3 venv
  $ source venv/bin/activate
  $ pip install -r requirements.txt
  ```

3. 建立名为 .env的环境参数配置文件，放置在项目根目录下：

  ```
  # .env

  #: Session对象需要该密钥
  SECRET_KEY=b77Os407FZ4i2Ybx%RzHV9LryW5^0pnc8Q5&he$h

  #: 你的邮箱地址，如果登入你的后台或者你的程序出错，该邮箱将警告或错误信息发到你的BLOG_ADMIN邮箱
  MAIL_USERNAME=example@gmail.com
  MAIL_PASSWORD=S7tRzzM!A8SC5w#$VU6@

  #: 这个邮箱地址可以接收警告或错误信息
  BLOG_ADMIN=example2@gmail.com

  #: 指定配置环境development/testing/production，默认dev环境
  BLOG_CONFIG=production

  #: 数据库地址
  DATABASE_URL=mysql://dbusername:@localhost/blogdb
  ```

4. 建立管理员帐号：

  ```
  (venv) $ python manage shell
  >>>  from app import db
  >>>  from app.models import User

  >>>  db.create_all()  #:创建表格

  >>>  user_admin = User(username='Admin', email='example@gmail.com')    #: 以创建一个Admin用户为例
  >>>  user_admin.password = 'E2^3$hWj$2GejVf8a7#d$u97pEW!tXW385IPDDPT'  #: 设置密码

  >>>  db.session.add(user_admin)  #: 添加用户到数据库
  >>>  db.session.commit()  #: 保存到数据库
  ```

  ​然后使用[example@gmail.com](mailto:example@gmail.com)和刚才设置的密码登入后台管理入口。（注意：登入密码需要保存好，你忘记了就永远找不回了）

