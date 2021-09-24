from flask import Flask
from flask import request
from flask import render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime

app = Flask(__name__)

# 使用 Flask-Bootstrap 的模板
bootstrap = Bootstrap(app)
# 渲染日期和时间
moment = Moment(app)

@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    # return '<h1>your browser is %s !</h1>' % user_agent
    # 渲染模板
    return render_template('index1.html', current_time=datetime.utcnow())

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

