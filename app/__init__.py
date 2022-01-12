from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# from flask_pagedown import PageDown
# 通过.pth文件解决导入问题。
import  config.config as config
from ext import mako
from app.models.baseModel import db
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
    # print(config.config[config_name]) 
    app.config.from_object(config.config[config_name])
    config.config[config_name].init_app(app)
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {'/i/': get_file_path()})

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    mako.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')




    return app


# print(config)



# app.config.from_object(config[config_name])
