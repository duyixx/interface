import unittest
import random

import ddt
import json
from decimal import Decimal

from common import requests_handler
from middlerware.handler import Handler

# 加载数据
handler = Handler()
test_data = handler.xls.read_data("invest")
# 用于写入用例执行结果
result_write = handler.xls.write_in_sheet("invest")
# 初始化日志
logger = handler.logger


@ddt.ddt
class TestInvest(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        # 普通用户登录
        cls.token = handler.token
        cls.member_id = handler.member_id
        logger.info("登录成功，member_id为：{}。开始执行提现接口的用例".format(cls.member_id))
        # admin登录
        cls.admin_token = handler.admin_token
        print("admin_token", cls.admin_token)

    @classmethod
    def tearDownClass(cls) -> None:
        logger.info("提现接口用例执行结束")

    def setUp(self) -> None:
        # 登录数据库
        self.db = handler.DbHandler()
        # 添加项目
        setattr(handler,"loan_id",handler.add_loan_id()[0])
        self.loan_id = handler.loan_id
        print("loanid", self.loan_id)
        # 审核项目
        handler.audit_loan()
        # 充值
        handler.recharge()

    def tearDown(self) -> None:
        self.db.close()

    @ddt.data(*test_data)
    def test_invest(self, test_info):
        cid = test_info["case_id"]
        ctl = test_info["title"]
        logger.info("执行用例：id: {}，title: {}".format(cid, ctl))
        result_write(cid + 1, 10, "此用例执行失败")  # 如果断言没有发生，则用例执行失败，为无效测试

        # 替换数据
        data = test_info["data"]
        # data =eval(data)
        if "#pass_loan_id#" in data:
            tem_pass_loan = self.db.query("SELECT * FROM futureloan.loan WHERE STATUS != 1 limit 1;")
            handler.pass_loan_id = str(tem_pass_loan[0]["id"])

        data = handler.replace_data(data)
        data = eval(data)  # 含有#sdf#形式的数据，需要它被替换后再用eval()

        # 替换token
        headers = test_info["headers"]
        headers = handler.replace_data(headers)
        headers = json.loads(headers)

        # sql_code = test_info["sql_code"]
        # if "#member_id#" in sql_code:
        # 	sql_code = sql_code.replace("#member_id#", str(self.member_id))
        # logger.info("数据处理成功")

        # 数据库数据获取
        # 查询之前的余额
        if test_info["sql_code"]:
            member = self.db.query("SELECT * FROM futureloan.member WHERE id = {}".format(self.member_id),one=True)
            money_before = member["leave_amount"]
        # 查询投资前的投资记录数
            before_loan = self.db.query(
                "SELECT * FROM futureloan.invest WHERE member_id = {}".format(self.member_id),
                one=False
            )

        # 访问接口
        print("headers", headers)
        print("data", data)
        res = requests_handler.visit(
            url=handler.yaml["host"] + test_info["url"],
            method=test_info["method"],
            headers=headers,
            json=data  # data用json.loads()不满足json格式时会报错，这时用eval
        )
        logger.info("请求发送成功")

        # 过滤前置条件不足的场景?

        # 断言
        expected = json.loads(test_info["expected"])
        print(res)

        try:
            self.assertEqual(expected["code"], res["code"], "id:{}返回码不符合预期".format(cid))
        except AssertionError as e:
            result_write(cid + 1, 10, "Fail：error code")
            raise e
        logger.info("返回码正确")
        try:
            self.assertEqual(expected["msg"], res["msg"], "id:{}返回状态信息不符合预期".format(cid))
        except AssertionError as e:
            result_write(cid + 1, 10, "Fail：error msg")
            raise e
        logger.info("返回状态信息正确")

        # 数据库校验
        if res["code"] == 0:
            after_loan = self.db.query(
                "SELECT * FROM futureloan.invest WHERE member_id = {}".format(self.member_id),
                one=False
            )
            # 断言投资是否增加一条
            self.assertTrue(len(before_loan)+1==len(after_loan))
            # 断言用户余额是否减少
            member_after = self.db.query("SELECT * FROM futureloan.member WHERE id = {}".format(self.member_id),one=True)
            money_after = member_after["leave_amount"]
            self.assertEqual(money_before-data["amount"],money_after)
        result_write(cid + 1, 10, "Pass")
