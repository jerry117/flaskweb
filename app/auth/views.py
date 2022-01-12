from flask_login import login_user, logout_user, current_user

from libs.utils import restful
from . import auth
from app.models.baseModel import db
from .models import User
from .forms import (LoginForm)


@auth.route('/login', methods=['POST'])
def login():
    '''登录'''
    form = LoginForm()
    if form.validate():
        # user = form.user
        # login_user(user, remember=True)
        # user_info, token = user.to_dict(), user.generate_reset_token()
        return restful.success('登录成功')
    return restful.fail(msg=form.get_error())

        
    
