from werkzeug.security import check_password_hash, generate_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from flask_login import UserMixin
from flask import current_app

from .. import login_manager
from app.models.baseModel import BaseModel, db
from config.config import conf

# roles_permissions = db.Table()


