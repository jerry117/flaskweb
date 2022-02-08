from unicodedata import name
from flask_login import current_user   # 匿名用户
from wtforms import StringField, IntegerField, Form
from wtforms.validators import ValidationError, Length, DataRequired

from app.auth.models import User, Role
from ..forms.baseForm import BaseForm


class CreateUserForm(BaseForm):
    '''创建用户的验证'''
    name = StringField(validators=[DataRequired('请设置用户名'), Length(2, 12, message='用户名长度为2~12位')])
    account = StringField(validators=[DataRequired('请设置账号'), Length(2, 50, message='账号长度为2~50位')])
    password = StringField(validators=[DataRequired('请设置密码'), Length(6, 18, message='密码长度长度为6~18位')])
    role_id = IntegerField(validators=[DataRequired('请选择角色')])

    def validate_name(self, field):
        '''校验用户名不重复'''
        if User.get_first(name=field.data):
            raise ValidationError(f'用户名 {field.data} 已存在')

    def validate_account(self, field):
        """校验账号不重复"""
        if User.get_first(account=field.data):
            raise ValidationError(f'账号 {field.data} 已存在')

    def validate_role_id(self, field):
        '''校验角色存在'''
        if Role.get_first(id=field.data):
            raise ValidationError(f'id为 {field.data} 的角色不存在')
                

class LoginForm(BaseForm):
    '''登录校验'''
    account = StringField(validators=[DataRequired('账号必填')])
    password = StringField(validators=[DataRequired('密码必填')])

    def validate_account(self, field):
        '''校验账号'''
        user = User.get_first(account=field.data)
        if user is None :
            raise ValidationError(f'账号错误')
        if user.status == 0:
            raise ValidationError(f'账号冻结')
        setattr(self, 'user', user)
        


