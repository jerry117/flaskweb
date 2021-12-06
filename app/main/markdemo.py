from flask import Flask, session, redirect, url_for, flash
from flask import request
from flask import render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import Form, FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required, DataRequired
from flask_sqlalchemy import SQLAlchemy
import os
# from flask_script import Manager,Shell
from flask_migrate import Migrate
from flask import Blueprint
# 应该是vscode的问题
# from __init__ import mail
from flask_mail import Message, Mail
from werkzeug.routing import BaseConverter
import urllib
from config import config


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__,template_folder='../templates', static_folder='../static')

# 使用 Flask-Bootstrap 的模板
bootstrap = Bootstrap(app)
# 渲染日期和时间
moment = Moment(app)
# 跨站请求伪造保护
app.config['SECRET_KEY'] = 'hard to guess string'
# 插件不兼容flask2.0的
# manager = Manager(app)
# mail.init_app(app)

# 简单的配置sqlite数据库
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = config.get('development').DB_URI
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
# 数据库的操作
# 初始化数据库  flask db init
# 自动创建迁移脚本   flask db migrate -m 'initial migration'
# 更新数据库 flask db upgrade
migrate = Migrate(app, db)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    # backref 在关系的另一个模型中添加反向引用  加入lazy=‘dynamic’参数，为了禁止自动执行查询
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name
    
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


class NameForm(FlaskForm):
    name = StringField('what is your name?', validators=[DataRequired()])
    submit = SubmitField('submit')

# @app.route('/')
# def index():
#     user_agent = request.headers.get('User-Agent')
#     # return '<h1>your browser is %s !</h1>' % user_agent
#     # 渲染模板
#     return render_template('index1.html', current_time=datetime.utcnow())


class ListConverter(BaseConverter):
    def __init__(self, url_map, separator='+'):
        super(ListConverter, self).__init__(url_map)
        # self.separator = urllib.unquote(separator)  #unquote  源码没有看到

    def to_python(self, value):
        return value.split(self.separator)

    def to_url(self, values):
        return self.separator.join(BaseConverter.to_url(value) for value in values ) 
        
        
app.url_map.converters['list'] = ListConverter

@app.route('/list1/<list:page_names>')
def list1(page_names):
    return 'separator: {} {}'.format('+', page_names)


@app.route('/list2/<list(separator=u"|"):page_names>')
def list2(page_names):
    return 'separator: {} {}'.format('|', page_names)
    




@app.route('/user/<name>')
def user(name):
    # return '<h1>hello %s !</h1>' % name
    # 使用渲染模板
    return render_template('user1.html', name=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


# @app.route('/', methods=['GET', 'POST'])
# def index():
#     name = None
#     form = NameForm()
#     if form.validate_on_submit():
#         name = form.name.data
#         form.name.data = ''
#     return render_template('index1.html', form=form, name=name, current_time=datetime.utcnow())


# @app.route('/', methods=['GET', 'POST'])
# def index():
#     form = NameForm()
#     if form.validate_on_submit():
#         session['name'] = form.name.data
#         return redirect(url_for('index'))
#     return render_template('index1.html', form=form, name=session.get('name'), current_time=datetime.utcnow())


@app.route('/', methods=['GET', 'POST'])
def index():
    # form = NameForm()
    # if form.validate_on_submit():
    #     old_name = session.get('name')
    #     if old_name is not None and old_name != form.name.data:
    #         flash('Looks like you have changed your name!')
    #     session['name'] = form.name.data
    #     # 重定向到这个地址
    #     return redirect(url_for('index'))
    # return render_template('index1.html', form = form, name = session.get('name'), current_time=datetime.utcnow())

    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        # 重定向到这个地址
        return redirect(url_for('index'))
    return render_template('index1.html', form = form, name = session.get('name'), known = session.get('known', False), current_time=datetime.utcnow())

# 唯一URLdemo

@app.route('/projects/')
def projects():
    return 'the project page'

# 访问http://127.0.0.1:5000/about/  会404
@app.route('/about')
def about():
    return 'the about page'
    

if __name__ == '__main__':
    app.run(debug=True)

# app.url_map  显示URL映射


# 上下文的使用例子
# from flask import current_app
# app_ctx = app.app_context()
# app_ctx.push()
# current_app.name
# app_ctx.pop()


# 支持的4种钩子
# • before_first_request：注册一个函数，在处理第一个请求之前运行。
# • before_request：注册一个函数，在每次请求之前运行。
# • after_request：注册一个函数，如果没有未处理的异常抛出，在每次请求之后运行。
# • teardown_request：注册一个函数，即使有未处理的异常抛出，也在每次请求之后运行。

# WTForms支持的HTML标准字段
# 字段类型        说　明
# StringField   文本字段
# TextAreaField  多行文本字段
# PasswordField  密码文本字段
# HiddenField    隐藏文本字段
# DateField      文本字段，值为 datetime.date 格式
# DateTimeField  文本字段，值为 datetime.datetime 格式
# IntegerField   文本字段，值为整数
# DecimalField   文本字段，值为 decimal.Decimal
# FloatField     文本字段，值为浮点数
# BooleanField   复选框，值为 True 和 False
# RadioField     一组单选框
# SelectField    下拉列表
# SelectMultipleField 下拉列表，可选择多个值
# FileField      文件上传字段
# SubmitField    表单提交按钮
# FormField      把表单作为字段嵌入另一个表单
# FieldList      一组指定类型的字段

# WTForms验证函数
# 验证函数        说　　明
# Email        验证电子邮件地址
# EqualTo      比较两个字段的值；常用于要求输入两次密码进行确认的情况
# IPAddress    验证 IPv4 网络地址
# Length       验证输入字符串的长度
# NumberRange  验证输入的值在数字范围内
# Optional     无输入值时跳过其他验证函数
# Required     确保字段中有数据
# Regexp       使用正则表达式验证输入值
# URL          验证 URL
# AnyOf        确保输入值在可选值列表中
# NoneOf       确保输入值不在可选值列表中


# 常用的SQLAlchemy关系选项
# 选项名         说　　明
# backref       在关系的另一个模型中添加反向引用
# primaryjoin   明确指定两个模型之间使用的联结条件。只在模棱两可的关系中需要指定
# lazy          指定如何加载相关记录。可选值有 select（首次访问时按需加载）、immediate（源对象加载后就加载）、joined（加载记录，但使用联结）、subquery（立即加载，但使用子查询），noload（永不加载）和 dynamic（不加载记录，但提供加载记录的查询）
# uselist       如果设为 Fales，不使用列表，而使用标量值
# order_by      指定关系中记录的排序方式
# secondary     指定多对多关系中关系表的名字
# secondaryjoin SQLAlchemy 无法自行决定时，指定多对多关系中的二级联结条件


# 跟运算符无关的特殊方法
# 类别                                   方法名
# 字符串/字节序列表示形式                 __repr__、__str__、__format__、__bytes__
# 数值转换                             __abs__、__bool__、__complex__、__int__、__float__、__hash__、__index__
# 集合模拟                             __len__、__getitem__、__setitem__、__delitem__、__contains__
# 迭代枚举                             __iter__、__reversed__、__next__
# 可调用模拟                           __call__
# 上下文管理                           __enter__、__exit__
# 实例创建和销毁                       __new__、__init__、__del__
# 属性管理                            __getattr__、__getattribute__、__setattr__、__delattr__、__dir__
# 属性描述符                          __get__、__set__、__delete__
# 跟类相关的服务                       __prepare__、__instancecheck__、__subclasscheck__



# 跟运算符相关的特殊方法
# 类别                               方法名和对应的运算符
# 一元运算符                      __neg__ -、__pos__ +、__abs__ abs()
# 众多比较运算符                   __lt__ <、__le__ <=、__eq__ ==、__ne__ !=、__gt__ >、__ge__ >=
# 算术运算符                      __add__ +、__sub__ -、__mul__ *、__truediv__ /、__floordiv__ //、__mod__ %、__divmod__ divmod()、__pow__ ** 或pow()、__round__ round()
# 反向算术运算符                   __radd__、__rsub__、__rmul__、__rtruediv__、__rfloordiv__、__rmod__、__rdivmod__、__rpow__
# 增量赋值算术运算符               __iadd__、__isub__、__imul__、__itruediv__、__ifloordiv__、__imod__、__ipow__
# 位运算符                        __invert__ ~、__lshift__ <<、__rshift__ >>、__and__ &、__or__ |、__xor__ ^
# 反向位运算符                    __rlshift__、__rrshift__、__rand__、__rxor__、__ror__
# 增量赋值位运算符                 __ilshift__、__irshift__、__iand__、__ixor__、__ior__


# GET：获取资源，GET操作应该是幂等的
# HEAD：想要获取信息，但是只关心消息头。应用应该像处理 GET 请求一样来处理它，但是不返回实际内容。
# POST：创建一个新的资源
# PUT：完整地替换资源或者创建资源。PUT操作虽然有副作用，但应该是幂等的
# DELETE：删除资源。DELETE操作有副作用，但也是幂等的
# OPTIONS：获取资源支持的所有 HTTP 方法。
# PATCH：局部更新，修改某个已有的资源


