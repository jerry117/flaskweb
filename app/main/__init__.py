from flask import Blueprint
# 先引入在给别的文件进行import
main = Blueprint('main', __name__)

from . import views, errors, forms
# from ..models import Permission
# from app.models import Permission




# @main.app_context_processor
# def inject_permissions():
#     return dict(Permission=None)





# 最后，相对导入只适用于在合适的包中的模块。尤其是在顶层的脚本的简单模块中，它们将不起作用。如果包的部分被作为脚本直接执行，那它们将不起作用 例如：
# python3 mypackage/A/spam.py # Relative imports fail


# 另一方面，如果你使用Python的-m选项来执行先前的脚本，相对导入将会正确运行。 例如：
# python3 -m mypackage.A.spam # Relative imports work