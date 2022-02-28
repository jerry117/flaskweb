import json
from collections import OrderedDict

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app.models.baseModel import db
from app.auth.models import User, Permission, Role
from app.api.config.models import Config, ConfigType
from manage import app

manager = Manager(app)

Migrate(app, db)
manager.add_command('db', MigrateCommand)

make_user_info_mapping = {
    '姓名':'name',
    '身份证号':'ssn',
    '手机号':'phone_number',
    '银行卡':'credit_card_number',
    '地址':'address',
    '公司名':'company',
    '统一社会信用代码':'credit_code',
    '邮箱':'company_email',
    '工作':'job',
    'ipv4':'ipv4',
    'ipv6':'ipv6',
}


kym_keword = [
    {
        "topic": "使用群体",
        "children": [
            {"topic": "产品使用群体是哪些？"},
            {"topic": "用户与用户之间有什么关联？"},
            {"topic": "用户为什么提这个需求？"},
            {"topic": "用户为什么提这个需求？"},
            {"topic": "用户最关心的是什么？"},
            {"topic": "用户的实际使用环境是什么？"}
        ]
    },
    {
        "topic": "里程碑",
        "children": [
            {"topic": "需求评审时间？"},
            {"topic": "开发提测时间？"},
            {"topic": "测试周期测试时间多长？"},
            {"topic": "轮次安排进行几轮测试？"},
            {"topic": "UAT验收时间？"},
            {"topic": "上线时间？"}
        ]
    },
    {
        "topic": "涉及人员",
        "children": [
            {"topic": "负责迭代的产品是谁？"},
            {"topic": "后端开发是谁经验如何？"},
            {"topic": "前端开发是谁经验如何？"},
            {"topic": "测试人员是谁？"}
        ]
    },
    {
        "topic": "涉及模块",
        "children": [
            {"topic": "项目中涉及哪些模块，对应的开发责任人是谁？"}
        ]
    },
    {
        "topic": "项目信息",
        "children": [
            {"topic": "项目背景是什么？"},
            {"topic": "这个项目由什么需要特别注意的地方？"},
            {"topic": "可以向谁进一步了解项目信息？"},
            {"topic": "有没有文档、手册、材料等可供参考？"},
            {"topic": "这是全新的产品还是维护升级的？"},
            {"topic": "有没有竞品分析结果或同类产品可供参考？"},
            {"topic": "历史版本曾今发生过那些重大故障？"}
        ]
    },
    {
        "topic": "测试信息",
        "children": [
            {"topic": "会使用到的测试账号有哪些？"},
            {"topic": "会用到的测试地址？"},
            {"topic": "有没有不太熟悉、掌握的流程？"}
        ]
    },
    {
        "topic": "设备工具",
        "children": [
            {"topic": "测试过程中是否会用到其他测试设备资源是否够（Ukey、手机、平板）？"},
            {"topic": "会用到什么测试工具会不会使用？"}
        ]
    },
    {
        "topic": "测试团队",
        "children": [
            {"topic": "有几个测试团队负责测试？"},
            {"topic": "负责测试的人员组成情况？"},
            {"topic": "测试人员的经验如何？"},
            {"topic": "测试人员对被测对象的熟悉程度如何？"},
            {"topic": "测试人员是专职的还是兼职的？"},
            {"topic": "测试人手是否充足？"}
        ]
    },
    {
        "topic": "测试项",
        "children": [
            {"topic": "主要的测试内容有哪些？"},
            {"topic": "哪部分可以降低优先级或者先不测试？"},
            {"topic": "哪些内容是新增或修改？"},
            {"topic": "是否涉及历史数据迁移测试？"},
            {"topic": "是否涉及与外系统联调测试？"},
            {"topic": "是否需要进行性能、兼容性、安全测试？"}
        ]
    }
]

@manager.command
def init_role(self):
    '''初始化权限、角色'''
    print()