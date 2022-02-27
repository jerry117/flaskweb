from unicodedata import name
from app.models.baseModel import BaseModel, db

class ConfigType(BaseModel):
    '''配置类型表'''

    __tablename__ = 'config_type'
    
    name = db.Column(db.String(128), nullable=True, unique=True, comment='字段名')
    desc = db.Column(db.String(128), nullable=True)