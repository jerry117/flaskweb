import json
from collections import OrderedDict

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app.models.baseModel import db
from app.auth.models import User, Permission, Role
# from app.

