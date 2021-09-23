from flask import make_response
from flask import Flask
from flask import redirect
from flask import abort



app = Flask(__name__)

@app.route('/')
def index():
    response = make_response('<h1>This document carries a cookie!</h1>')
    response.set_cookie('answer', '43')
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


    
if __name__ == '__main__':
    app.run(debug=True)