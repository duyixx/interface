import unittest
import random

import ddt
import json
from decimal import Decimal

from common import requests_handler
from middlerware.handler import Handler

# 加载数据
handler = Handler()
test_data = handler.xls.read_data("audit")
# 用于写入用例执行结果
result_write = handler.xls.write_in_sheet("audit")
# 初始化日志
logger = handler.logger


@ddt.ddt
class TestAudit(unittest.TestCase):

	@classmethod
	def setUpClass(cls) -> None:
		# 普通用户登录
		cls.token = handler.token
		cls.member_id = handler.member_id
		logger.info("登录成功，member_id为：{}。开始执行提现接口的用例".format(cls.member_id))
		# admin登录
		cls.admin_token = handler.admin_token
		print("admin_token",cls.admin_token)

	@classmethod
	def tearDownClass(cls) -> None:
		logger.info("提现接口用例执行结束")

	def setUp(self) -> None:
		# 登录数据库
		self.db = handler.DbHandler()
		# 添加项目
		self.loan_id = handler.loan_id
		print("loanid",self.loan_id)
	def tearDown(self) -> None:
		self.db.close()


	@ddt.data(*test_data)
	def test_audit(self, test_info):
		cid = test_info["case_id"]
		ctl = test_info["title"]
		logger.info("执行用例：id: {}，title: {}".format(cid, ctl))
		result_write(cid+1, 10, "此用例执行失败")  # 如果断言没有发生，则用例执行失败，为无效测试

		# 替换数据
		data = test_info["data"]
		# if "#loan_id#" in data:
		# 	data = data.replace("#loan_id#", str(self.loan_id))
		if "#pass_loan_id#" in data:
			tem_pass_loan = self.db.query("SELECT * FROM futureloan.loan WHERE STATUS != 1 limit 1;")
			handler.pass_loan_id = str(tem_pass_loan[0]["id"])

		data=handler.replace_data(data)

		data = eval(data)	 # json.loads()方式不能处理数字，故用eval()

		headers = test_info["headers"]
		if "#admin_token#" in headers:
			headers = headers.replace("#admin_token#", self.admin_token)

		headers = eval(headers)
		# sql_code = test_info["sql_code"]
		# if "#member_id#" in sql_code:
		# 	sql_code = sql_code.replace("#member_id#", str(self.member_id))
		# logger.info("数据处理成功")

		# 数据库数据获取
		# user_info = self.db.query(sql_code)
		# before_amount = user_info[0]['leave_amount']  # :返回的是Decimal类型

		# 访问接口
		print("headers",headers)
		print("data",data)
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
			result_write(cid+1,10,"Fail：error code")
			raise e
		logger.info("返回码正确")
		try:
			self.assertEqual(expected["msg"], res["msg"], "id:{}返回状态信息不符合预期".format(cid))
		except AssertionError as e:
			result_write(cid+1,10,"Fail：error msg")
			raise e
		logger.info("返回状态信息正确")

		# 数据库校验
		if res["code"] == 0:
			loan = self.db.query(test_info["sql_code"].format(self.loan_id),one=True)
			self.assertTrue(loan["status"],expected["status"])
			logger.info("id:{}，title:{}，PASS。数据库校验通过".format(cid,ctl))
			# handler.pass_loan_id = loan["id"]  # 存储不在审核状态的项目的id
		else:
			logger.info("id:{}，title:{}，PASS".format(cid,ctl))
		result_write(cid+1,10,"Pass")

