# from datetime import datetime
# from hashlib import new
# from operator import truediv
# from os import abort
# from flask import json, render_template, session, redirect, url_for, jsonify, send_file, request
# from libs.utils.utils import get_file_path, humanize_bytes
# from . import main
# from .forms import NameForm
# from .. import db, mako
# # 需要使用这个来进行模块的使用验证python3 -m app.main.views
# # from app.models.models import PasteFile, User
# import os

# ONE_MONTH = 60 * 60 * 24 * 30

# @main.route('/', methods=['GET', 'POST'])
# def index():
#     # form = NameForm()
#     # if form.validate_on_submit():
#     #     session['name'] = form.name.data
#     #     return redirect(url_for('.index'))
#     # return render_template('index1.html', form=form, name=session.get('name'), current_time=datetime.utcnow())
#     form = NameForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.name.data).first()
#         if user is None:
#             user = User(username=form.name.data)
#             db.session.add(user)
#             session['known'] = False
#         else:
#             session['known'] = True
#         session['name'] = form.name.data
#         form.name.data = ''
#         # 重定向到这个地址  加.为了指向当前的地址不然会找到main里的index
#         return redirect(url_for('.index'))
#     return render_template('index1.html', form = form, name = session.get('name'), known = session.get('known', False), current_time=datetime.utcnow())


# @main.route('/user/<name>')
# def user(name):
#     # return '<h1>hello %s !</h1>' % name
#     # 使用渲染模板
#     return render_template('user/user1.html', name=name)


# @main.route('/index1/', methods=['GET', 'POST'])
# def index1():
#     if request.method == 'POST':
#         uploaded_file = request.files['file']
#         w = request.form.get('w')
#         h = request.form.get('h')
#         if not uploaded_file:
#             return abort(400)

#         if w and h:
#             paste_file = PasteFile.rsize(uploaded_file, w, h)
#         else:
#             paste_file = PasteFile.create_by_upload_file(uploaded_file)
#         db.session.add(paste_file)
#         db.session.commit()


#         return jsonify({
#             'url_d': paste_file.url_d,
#             'url_i': paste_file.url_i,
#             'url_s': paste_file.url_s,
#             'url_p': paste_file.url_p,
#             'filename': paste_file.filename,
#             'size': humanize_bytes(paste_file.size),
#             'time': str(paste_file.upload_time),
#             'type': paste_file.type,
#             'quoteurl': paste_file.quoteurl,

#         })
#     return render_template('index2.html', **locals())
    
# @main.route('/r/<img_hash>')
# def rsize(img_hash):
#     w = request.args.get('w')
#     h = request.args.get('h')

#     old_paste = PasteFile.get_by_filehash(img_hash)
#     new_paste = PasteFile.rsize(old_paste, w, h)

#     return new_paste.url_i


# @main.route('/d/<filehash>', methods=['GET'])  
# def download(filehash):
#     paste_file = PasteFile.get_by_filehash(filehash)
#     return send_file(open(paste_file.path, 'rb'), mimetype='application/octet-stream', cache_timeout=ONE_MONTH, as_attachment=True, attachment_filename=paste_file.filename.encode('utf-8'))


# @main.route('/p/<filehash>')
# def preview(filehash):
#     paste_file = PasteFile.get_by_filehash(filehash)

#     if not paste_file:
#         filepath = get_file_path((filehash))
#         if not (os.path.exists(filepath)) and (not os.path.islink(filepath)):
#             return abort(404)
#         paste_file = PasteFile.create_by_old_paste(filehash)
#         db.session.add(paste_file)
#         db.session.commit()
    
#     return render_template('success.html', p=paste_file)

# @main.route('/s/<symlink>')
# def s(symlink):
#     paste_file = PasteFile.ge
#     return redirect(paste_file.url_p)

# @main.route('/j/', methods=['POST'])
# def j():
#     uploaded_file = request.files['file']

#     if uploaded_file:
#         paste_file = PasteFile.create_by_upload_file(uploaded_file)
#         db.session.add(paste_file)
#         db.session.commit()
#         width, height = paste_file.image_size

#         return jsonify({
#             'url': paste_file.url_i,
#             'short_url': paste_file.url_s,
#             'origin_filename': paste_file.filename,
#             'hash': paste_file.filehash,
#             'width': width,
#             'height': height
#         })
#     return abort(400)


# @main.after_request
# def after_request(response):
#     response.headers['Access-Control-Allow-Origin'] = '*'
#     response.headers['Access-Control-Allwo-Headers'] = 'Content-Type'
#     return response





# # @app.route('/', methods=['GET', 'POST'])
# # def index():
# #     form = NameForm()
# #     if form.validate_on_submit():
# #         session['name'] = form.name.data
# #         return redirect(url_for('index'))
# #     return render_template('index1.html', form=form, name=session.get('name'), current_time=datetime.utcnow())