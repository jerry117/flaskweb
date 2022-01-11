from flask import views


from libs.utils.required import *


class BaseMethodView(views.MethodView):
    decorators = [login_required]


class AdminMethodView(BaseMethodView):
    decorators = [login_required, admin_required]