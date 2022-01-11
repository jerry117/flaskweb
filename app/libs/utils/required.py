# 使用wraps创建装饰器时保留函数元信息  
from functools import wraps

from flask import request
from flask_login import current_user

from app.auth.models import User
from app.libs.utils import restful


def login_required(func):
    '''校验用户登录状态'''

    @wraps(func)
    def decorated_view(*args, **kwargs):
        return func(*args, **kwargs) if User.pa
        
    return decorated_view