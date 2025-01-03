import os
from flask import Flask, jsonify
from flask_mail import Mail
from flask_cors import CORS
from flask_session import Session

mail = Mail()
# 获取当前工作目录，即 flaskr 所在目录
base_dir = os.path.dirname(os.path.abspath(__file__))

# 设置相对路径到 session 文件夹
session_dir = os.path.join(base_dir, '..', 'flask_session')


# 应用工厂函数
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app, origins=["http://113.44.59.183"], supports_credentials=True)  # 允许跨域
    app.config.from_mapping(
        SECRET_KEY='aovdnfdp',
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SECURE=False,
        SESSION_PERMANENT=False,
        SESSION_COOKIE_DOMAIN='.113.44.59.183',
        SESSION_COOKIE_SAMESITE=None,
        SESSION_COOKIE_PATH='/',
        SESSION_FILE_DIR=session_dir,
        SESSION_TYPE='filesystem',  # 使用文件系统存储 session
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        SECURITY_PASSWORD_SALT='mysecretpasswordsalt',  # 设定你的盐值
        MAIL_SERVER='smtp.163.com',
        MAIL_PORT=25,
        MAIL_USE_TLS=True,
        MAIL_USERNAME='xhc926@163.com',
        MAIL_PASSWORD='SGexfqvdsYqVigam',
    )
    # 初始化 Flask-Session
    Session(app)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello/')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)
    with app.app_context():
        db.init_db()

    # 初始化邮件实例
    mail.init_app(app)
    # 认证蓝图：注册新用户、登录和注销视图
    from . import auth
    app.register_blueprint(auth.bp)

    # 博客蓝图：列出帖子 创建、修改删除帖子
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')
    # url_for('index) 或 url_for('blog.index') 生成同样的/url

    # 个人中心蓝图：查看、修改个人信息
    from . import profile
    app.register_blueprint(profile.bp)

    # 管理员中心蓝图
    from . import admin
    app.register_blueprint(admin.bp)
    return app
