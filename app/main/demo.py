from flask import Flask, url_for, request, jsonify, render_template, abort, redirect, make_response, g
from flask.views import View
from flask.wrappers import Request
from markdown import user
from werkzeug.wrappers import Response
import pymysql
from sqlalchemy import create_engine
from config import config


app = Flask(__name__, template_folder='../templates')
app.config.from_object('config')
eng = create_engine(config.get('development').DB_URI)


class JsonResponse(Response):
    @classmethod
    def force_type(cls, rv, environ=None):
        if isinstance(rv, dict):
            rv = jsonify(rv)
        return super(JsonResponse, cls).force_type(rv, environ)
        
app.response_class = JsonResponse

@app.url_value_preprocessor
def get_site(endpoint, values):
    g.site = values.pop('subdomain')

@app.route('/2/', subdomain='<subdomain>')
def index2():
    return g.site
        


@app.route('/')
def index():
    response = make_response('<h1>This document carries a cookie!</h1>')
    response.set_cookie('answer', 'Jerry')
    return response

# 重定向demo
@app.route('/baidu')
def index1():
    return redirect('http://www.baidu.com')

# abort通过处理错误，把404接管给web服务器
@app.route('/user/<id>')
def get_user(id):
    # user = load_user(id)
    user = False
    if not user:
        abort(404)
    return '<h1>Hello, %s</h1>' % user.name

@app.route('/item/1/')
def item(id):
    pass

@app.route('/people/')
def people():
    name = request.args.get('name')
    if not name:
        return redirect(url_for('login'))
    user_agent = request.headers.get('User-Agent')
    return 'name: {} ; ua: {}'.format(name, user_agent)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form.get['user_id']
        return 'user:{} login'.format(user_id)
    else:
        return 'open login page'

@app.route('/secret/')
def secret():
    abort(401)
    print('this is never executed')
    
    
    
@app.route('/1/')
def hello_world():
    return {'message': 'hello world!'}
    
@app.route('/custom_headers/')
def headers():
    return {'headers': [1,2,3]}, 201, [('X-Request-Id', '100')]

with eng.connect() as con:
    rs = con.execute('select * from user;')
    for row in rs:
        print(row)

# test_request_context 在交互模式下产生请求上下文
with app.test_request_context():
    print(url_for('item', id='1'))
    print(url_for('item', id=2, next='/'))
    print(config.get('development').DB_URI)    
    
if __name__ == '__main__':
    app.run(debug=app.debug)