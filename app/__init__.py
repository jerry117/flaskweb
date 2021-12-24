from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# from flask_pagedown import PageDown
# 通过.pth文件解决导入问题。
from config import config
from ext import db, mako
from libs.utils.utils import get_file_path
from werkzeug.middleware.shared_data import SharedDataMiddleware

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
# db = SQLAlchemy()
# pagedown = PageDown()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = u'请登录后操作'  #设置登录提示消息
login_manager.login_message_category = 'info' #设置消息分类

def create_app(config_name):
    # app = Flask(__name__)
    app = Flask(__name__,template_folder='templates', static_folder='static')
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {'/i/': get_file_path()})

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    mako.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app


# print(config)



# app.config.from_object(config[config_name])
