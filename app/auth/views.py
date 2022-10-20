from flask_login import login_user, logout_user, current_user
from flask.views import View, MethodView
from libs.utils import restful
from . import auth
from app.models.baseModel import db
from .models import User
from .forms import (LoginForm)

# 通过装饰器来注册路由
@auth.route('/login', methods=['POST'])
def login():
    '''登录'''
    form = LoginForm()
    if form.validate():
        user = form.user
        login_user(user, remember=True)
        user_info, token = user.to_dict(), user.generate_reset_token()
        user_info['token'] = token
        return restful.success('登录成功', user_info)
    return restful.fail(msg=form.get_error())

# 跟装饰器注册路由逻辑一样
def Login():
    """登录"""
    return {'hello': 'world'}

auth.add_url_rule('/hello', view_func=Login)

# 可插拔视图，基于类的视图
class MyView(MethodView):
    def get(self):
        return {'code': 0, "msg": 'get 请求'}
    
    def post(self):
        return {'code': 0, "msg": 'post 请求'}

auth.add_url_rule("/my", view_func=MyView.as_view('myview'))