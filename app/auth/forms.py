from flask_login import current_user   # 匿名用户
from wtforms import StringField, IntegerField, Form
from wtforms.validators import ValidationError, Length, DataRequired

