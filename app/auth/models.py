from os import name
from werkzeug.security import check_password_hash, generate_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from flask_login import UserMixin, current_user
from flask import current_app

from .. import login_manager
from app.models.baseModel import BaseModel, db
from config.config import conf

# 角色与权限映射表
roles_permissions = db.Table(
    'roles_permissions',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id')))


class Role(BaseModel):
    __tablename__ = 'role'
    name = db.Column(db.String(30), unique=True, comment='角色名称')
    users = db.relationship('User', back_populates='role')
    permission = db.relationship('Permission', secondary=roles_permissions, back_populates='role')

class Permission(BaseModel):
    """ 角色对应的权限 """
    __tablename__ = 'permission'
    name = db.Column(db.String(30), unique=True, comment='权限名称')
    role = db.relationship('Role', secondary=roles_permissions, back_populates='permission')


class User(UserMixin, BaseModel):
    """ 用户表 """
    __tablename__ = 'users'
    account = db.Column(db.String(50), unique=True, index=True, comment='账号')
    password_hash = db.Column(db.String(255), comment='密码')
    name = db.Column(db.String(12), comment='姓名')
    status = db.Column(db.Integer, default=1, comment='状态，1为启用，2为冻结')
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), comment='所属的角色id')
    role = db.relationship('Role', back_populates='users')

    @property
    def password(self):
        return self.password_hash
    
    @password.setter
    def password(self, _password):
        """ 设置加密密码 """
        self.password_hash = generate_password_hash(_password)


    def verify_password(self, password):
        """ 校验密码 """
        return check_password_hash(self.password_hash, password)