# My blog with Flask

简单记录一下自己Flask blog搭建过程。

自己的blog之路： Lofter  -->  WordPress --> google blog  --> github.io  --> flask blog。

七月中旬对着[《Flask Web开发》](https://book.douban.com/subject/25814739/)一字不落的敲完代码，对于flask框架算是入门，于是寻思着将github.io上的blog使用现学的flask替代，还是自己折腾的有成就感。

前前后后从开始框架搭建到后面部署到vps上，初步完成大概花了一周的时间。后来又慢慢调整页面布局，对自己不理解的地方在重新理一遍。

此次搭建特别感谢[laike9m](https://laike9m.com/)，前端设计来自其博客，发现这位大佬的博客应该是gitbook上看[leetcode题解](https://algorithm.yuanbin.me/zh-hans/)的时候，template 出处是[css3teamplate](http://www.css3templates.co.uk/), 程序的架构布局参照[Miguel Grinberg](https://blog.miguelgrinberg.com/)的《Flask Web开发》。



## 项目架构

blog架构如图：

![image](https://github.com/purelind/glowing-octo-potato/blob/master/app/static/CSS3_two/images/blogskeleton.png)

这种结构有6个顶级文件夹：

- blog程序一般都保存在`app`下；
- `dist` 文件夹保存程序版本备份；
- `log`文件夹保存错误信息；
- `migrations` 文件夹包含数据迁移脚本；
- `tests`文件夹保存单元测试；
- `venv`文件夹则包含Python虚拟环境。

此外创建的新文件有：

- `requirements.text`列出了所有的依赖；
- `config.py`存储配置；
- `gunicorn.conf`存储部署时候gunicorn的启动参数；
- `manage.py`用于启动程序以及其他的程序任务；
- `LICENSE`和`README.md`则是属于github的文件。

blog的程序主要在app文件夹中：

- 不同的程序功能，使用不同的蓝本，与系统认证系统相关的路由在`auth`蓝本中定义；
- `main`文件夹用于保存主要的蓝本，关于blueprint的话，详细了解见这里；
- `static`用于存放静态文件，css、js、图片；
- `__init__.py`构造文件
- 数据库模型：`models.py`



## 后端

后端配置参照《Flask Web开发》，简单挑几个点说：

* 关于`Flask-Bootstrap`，刚开始直接使用`flask-bootstrap`集成的Twitter Bootstrap，后来想要尝试不同的前端页面风格，于是改用`w3.css`.但是没有完全抛弃bootstrap,自己在独立渲染`admin`的表单时，发现表单数据不能正常提交给数据库，而使用bootstrap/wtf.html文件定义的辅助函数则可以。于是直接取看wtf.html的源码，没能理清其辅助函数如何工作的。日后再尝试将表单渲染问题解决；
* 数据库使用**mariadb**，开发环境是**debian9**，上面的默认数据库是mariadb;
* blog的分类和标签功能现在没有实现
* 关于admin管理，尝试过使用`flask-admin`，其功能和界面相比自己目前简陋的管理界面号太多，但是在将flask-admin适配自己的blog时，发现并不简单，在处理login认证的时候则让我放弃使用了。不过期间遇到了循环引用的问题，之前看书的时候理解不深。





## 前端

前端模块来之css3template，在看到laike9m的博客时，喜欢那样的布局，而且其博客代码开源，于是想着利用flask搭建这样博客。看过其博客的github源码时，面对着html、css、js的时候则懵了。于是赶紧回去[w3school](https://www.w3schools.com/)补补网页前端的基础，没有入门知识，照抄也是会出问题的，而且你花在不断的google的时间会很多还不一定可以解决问题，而这些小问题当自己完整的过一遍基础教程则很容易避免。

前端的几个问题简单记录一下：

* 页面的底部状态栏浮动置底的问题一直没有解决好，可能通过js处理会相对容易，目前js水平太次，于是通过固定侧边栏高度来暂时处理；
* 引入了**disqus**评论后，发现如果文章过短，评论就直接跑到页面中间，　日后想实现disqus评论手动点开才张开，这是在[dtysky](http://dtysky.moe/)的博客发现的，觉得这是个不错的功能，可以进一步减少阅读时候的干扰；
* 对于移动端支持太差；



## 部署

关于部署，首先是主机的选择了: 自己使用的是Linode最低配的vps，系统用的是debian。之前为了上youtube将vultur,digitocean,banwagong还有linode全都尝试了一遍，目前主要使用Linode。如果熟悉基础linux操作，vps是个更好的选择，自己动手折腾乐趣多多，部署过程中的许多坑可以自己体验。

其他选择就是《Flask Web开发》书中提及的PaaS，Heroku就是其中之一，可以提供一定的免费服务。

部署需要记录的关键点：

* nginx的配置
* https证书的申请和配置