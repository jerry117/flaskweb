from datetime import datetime
from os import abort
from flask import render_template, session, redirect, url_for, jsonify
from libs.utils.utils import humanize_bytes
from werkzeug.wrappers import request
from . import main
from .forms import NameForm
from .. import db
# 需要使用这个来进行模块的使用验证python3 -m app.main.views
from ..models import PasteFile, User

@main.route('/', methods=['GET', 'POST'])
def index():
    # form = NameForm()
    # if form.validate_on_submit():
    #     session['name'] = form.name.data
    #     return redirect(url_for('.index'))
    # return render_template('index1.html', form=form, name=session.get('name'), current_time=datetime.utcnow())
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


@main.route('/user/<name>')
def user(name):
    # return '<h1>hello %s !</h1>' % name
    # 使用渲染模板
    return render_template('user1.html', name=name)


@main.route('/i/', methods=['GET', 'POST'])
def index1():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        w = request.form.get('w')
        h = request.form.get('h')
        if not uploaded_file:
            return abort(400)

        if w and h:
            paste_file = PasteFile.rsize(uploaded_file, w, h)
        else:
            paste_file = PasteFile.create_by_upload_file(uploaded_file)
        db.session.add(paste_file)
        db.session.commit()


        return jsonify({
            'url_d': paste_file.url_d,
            'url_i': paste_file.url_i,
            'url_s': paste_file.url_s,
            'url_p': paste_file.url_p,
            'filename': paste_file.filename,
            'size': humanize_bytes(paste_file.size),
            'time': str(paste_file.upload_time),
            'type': paste_file.type,
            'quoteurl': paste_file.quoteurl,

        })
    return render_template(index2.html, **locals())
    

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     form = NameForm()
#     if form.validate_on_submit():
#         session['name'] = form.name.data
#         return redirect(url_for('index'))
#     return render_template('index1.html', form=form, name=session.get('name'), current_time=datetime.utcnow())