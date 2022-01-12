from datetime import datetime
from werkzeug.exceptions import abort

from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery, Pagination
from sqlalchemy import MetaData
from contextlib import contextmanager

from config.config import conf
from libs.utils.jsonUtil import JsonUtil



class SQLAlchemy(_SQLAlchemy):

    @contextmanager
    def auto_commit(self):
        try:
            yield 
            self.session.commit()
        except Exception as error :
            db.session.rollback()
            raise error
    
    def execute_query_sql(self, sql):
        '''查询，返回字典'''
        res = self.session.execute(sql).fetchall()
        return dict(res) if res else {}
        

class  Qeury(BaseQuery):
    '''重写query方法，使其默认加上status=0'''
    def filter_by(self, **kwargs):
        '''如果传过来的参数中不含is_delete，则默认加一个is_delete参数，状态为0 查询有效的数据'''
        # kwargs.setdefault('is_delete', 0)
        return super(Qeury, self).filter_by(**kwargs)

    def paginate(self, page=1,  per_page=20, error_out=True, max_per_page=None):
        '''重写分页器，页码页数强制转成int， 解决服务器int识别str导致分页报错的问题'''
        page, per_page = int(page) or conf['page']['pageNum'], int(per_page) or conf['page']['pageSize']
        if max_per_page is not None:
            per_page = min(per_page, max_per_page)
        items = self.limit(per_page).offset((page - 1) * per_page).all()
        if not items and page != 1 and error_out:
            abort(404)
        total = self.order_by(None).count()
        return Pagination(self, page, per_page, total, items)


# 由于数据库迁移的时候，不兼容约束关系的迁移，下面是百度出的解决方案
naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}


db = SQLAlchemy(query_class=Qeury, metadata=MetaData(naming_convention=naming_convention), use_native_unicode='utf8mb4')


class BaseModel(db.Model, JsonUtil):
    '''基类模型'''
    __abstract__ = True
    # 考虑一下integer是否需要加括号。
    id = db.Column(db.Integer, primary_key=True, comment='自增主键')
    created_time = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    updated_time = db.Column(db.DateTime, default=datetime.now, comment='修改时间', onupdate=datetime.now)
    created_user = db.Column(db.Integer, nullable=True, default=1, comment='创建数据的用户ID')
    updated_user = db.Column(db.Integer, nullable=True, default=1, comment='修改数据的用户ID')

    @property
    def str_created_time(self):
        return datetime.strftime(self.created_time, "%Y-%m-%d %H:%M:%S")


    @property
    def str_update_time(self):
        return datetime.strftime(self.updated_time, "%Y-%m-%d %H:%M:%S")
    
    def create(self, attrs_dict: dict, *args):
        with db.auto_commit():
            try:
                setattr(self, 'create_user', current_user.id)
                setattr(self, 'update_user', current_user.id)
            except Exception as error :
                pass
            for key, value in attrs_dict.items():
                if hasattr(self, key) and key != 'id':
                    setattr(self, key, self.dumps(value) if key in args else value)
            db.session.add(self)
        return self

    def update(self, attrs_dict:dict, *args):

        try:
            setattr(self, 'update_user', current_user.id)
        except Exception as error :
            pass
        with db.auto_commit():
            for key, value in attrs_dict.items():
                if hasattr(self, key) and key not in ['id', 'num']:
                    setattr(self, key, self.dumps(value) if key in args else value)
        
    def is_create_user(self, user_id):
        return self.created_user == user_id

    @classmethod
    def get_first(cls, **kwargs):
        return cls.query.filter_by(**kwargs).first()


    @classmethod
    def get_all(cls, **kwargs):
        return cls.query.filter_by(**kwargs).all()

    @classmethod
    def get_filter_by(cls, **kwargs):
        return cls.query.filter_by(**kwargs)

    @classmethod
    def get_filter(cls, **kwargs):
        return cls.query.filter(**kwargs)
        
    @classmethod
    def change_sort(cls, id_list, page_num, page_size):
        with db.auto_commit(): 
            for index, case_id in enumerate(id_list):
                case = cls.get_first(id=case_id)
                case.num = (page_num - 1) * page_size + index
               
    @classmethod
    def to_dict(self, to_dict:list = [], pop_list:list = []):
        dict_data = {}
        pop_list.extend(['created_time', 'update_time'])
        for column in self.__table__.columns:
            if column.name not in pop_list:
                data = getattr(self, column.name)
                dict_data[column.name] = data if column.name not in to_dict else self.loads(data)
        dict_data.update({'created_time': self.str_created_time, 'update_time': self.str_update_time})
        return dict_data

    