from flask import Flask, session, redirect, url_for, flash
from flask import request
from flask import render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# 使用 Flask-Bootstrap 的模板
bootstrap = Bootstrap(app)
# 渲染日期和时间
moment = Moment(app)
# 跨站请求伪造保护
app.config['SECRET_KEY'] = 'hard to guess string'

# 简单的配置sqlite数据库
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name
    
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


class NameForm(Form):
    name = StringField('what is your name?', validators=[Required()])
    submit = SubmitField('submit')

# @app.route('/')
# def index():
#     user_agent = request.headers.get('User-Agent')
#     # return '<h1>your browser is %s !</h1>' % user_agent
#     # 渲染模板
#     return render_template('index1.html', current_time=datetime.utcnow())

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
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index1.html', form = form, name = session.get('name'), current_time=datetime.utcnow())


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