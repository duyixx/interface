"""
功能：初始化所有数据，在其他模块从common中实例化对象时可以重复使用这些数据。
"""
import os

from jsonpath import jsonpath
from pymysql.cursors import DictCursor
from common import yaml_handler, logging_handler, requests_handler
from common.mysql_handler import MySQLHandler
from config import config
from common import excel_handler


# 重写MySQLHandler以简化链接数据库的代码
class MySQLHandlerMid(MySQLHandler):
    def __init__(self):
        db_config = Handler.yaml["db"]
        super().__init__(
            host=db_config["host"],
            port=db_config["port"],
            user=db_config["user"],
            password=db_config["password"],
            charset=db_config["charset"],
            cursorclass=DictCursor
        )


# 一个测试文件共用的数据对象：config、yaml、Excel、logger，使用一个类来封装
class Handler(object):
    loan_id = None
    # 加载配置项
    conf = config

    # 加载yaml
    yaml = yaml_handler.read_yaml(os.path.join(conf.CONFIG_PATH, "config.yml"))

    # 加载excel数据
    __case_path = conf.DATA_PATH
    __case_file = yaml["excel"]["test_datafile"]
    xls = excel_handler.ExcelHandler(os.path.join(__case_path, __case_file))

    # 加载logger
    __logger_config = yaml["logger"]
    logger = logging_handler.LoggerHandler(
        logger_name=__logger_config["logger_name"],
        logger_level=__logger_config["logger_level"],
        file_name=os.path.join(config.LOG_PATH, __logger_config["file_name"]),
        file_level=__logger_config["file_level"],
        stream_level=__logger_config["stream_level"],
        fmt='%(asctime)s-%(filename)s-->line:%(lineno)d-%(levelname)s:%(message)s'
    )
    # mysql不放在Handler里面，因为每个用例有各自的数据库对象
    # 这里写入便于统一用Handler类进行管理
    DbHandler = MySQLHandlerMid

    def replace_data(self, data):
        import re
        pattern = r"#(.*?)#"
        while re.search(pattern, data):
            key = re.search(pattern, data).group(1)
            value = getattr(self, key, "")
            data = re.sub(pattern, str(value), data, 1)
        return data

    def login(self, user_to_login):
        """登录测试账号，正好将登录的入参封装了"""
        res = requests_handler.visit(
            url=Handler.yaml["host"] + "/member/login",
            method="post",
            headers={"X-Lemonban-Media-Type": "lemonban.v2"},
            json=self.yaml[user_to_login]
        )
        # # 提取token
        # token_str = res["data"]["token_info"]["token"]
        # token_type = res["data"]["token_info"]["token_type"]
        # token = " ".join([token_type, token_str])
        # # 提取member_id
        # member_id = res["data"]["id"]

        # 使用jsonpath提取token和member_id
        token = jsonpath(res, "$..token_type")[0] + " " + jsonpath(res, "$..token")[0]
        member_id = jsonpath(res, "$..id")[0]
        return {"token": token, "member_id": member_id}

    def add_loan_id(self):
        # 新建项目并提取项目id
        # 新建项目的入参
        data = {
            "member_id": self.member_id,
            "title": "用例前置条件创建的项目",
            "amount": 2000,
            "loan_rate": 12.0,
            "loan_term": 3,
            "loan_date_type": 1,
            "bidding_days": 5
        }
        # 发送请求，添加项目
        res = requests_handler.visit(
            url=Handler.yaml["host"] + "/loan/add",
            method="post",
            headers={"Authorization": self.token, "X-Lemonban-Media-Type": "lemonban.v2"},
            json=data
        )
        # 返回项目id
        return jsonpath(res, "$..id")

    @property
    def token(self):
        return self.login("user")["token"]

    @property
    def member_id(self):
        return self.login("user")["member_id"]

    @property
    def admin_token(self):
        return self.login("admin_user")["token"]

    # @property
    # def loan_id(self):
    #     return self.add_loan_id()[0]

    pass_loan_id = ""

    def audit_loan(self):
        """审核项目"""
        data = {"loan_id":self.loan_id, "approved_or_not":True}
        resp = requests_handler.visit(
            url=Handler.yaml["host"] + "/loan/audit",
            method="patch",
            headers={"Authorization":self.admin_token,"X-Lemonban-Media-Type":"lemonban.v2"},
            json = data
        )
        print("审核项目",resp)

    def recharge(self):
        """充值"""
        data = {"member_id": self.member_id, "amount":500000}

        resp = requests_handler.visit(
            url=Handler.yaml["host"] + "/member/recharge",
            method="post",
            headers={"Authorization":"#token#","X-Lemonban-Media-Type":"lemonban.v2"},
            json = data
        )


if __name__ == '__main__':

    handler = Handler()
    # print(handler.conf.ROOT_PATH)
    # print(handler.yaml["logger"])
    # print(handler.xls.read_data("login"))
    # handler.logger.info("110")
    #
    # db = MySQLHandlerMid()
    # print(db)
    # db2 = handler.DbHandler()
    # print(db2)
    # print(isinstance(db2,MySQLHandler))
    # print(login())
    str1 = '"member_id"：#member_id#， "token"："#token#"，"loan_id"：#loan_id#,' \
           '"admin_token":#admin_token#, "random_prop":#random# '
    print(handler.replace_data(str1))


