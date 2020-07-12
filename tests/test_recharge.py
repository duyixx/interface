import unittest
import random

import ddt
import json
from decimal import Decimal

from common import requests_handler
from middlerware.handler import Handler,login

# 加载数据
handler = Handler()
test_data = handler.xls.read_data("recharge")

@ddt.ddt
class TestWithdraw(unittest.TestCase):

	@classmethod
	def setUpClass(cls) -> None:
		# 登录:所有充值用例都要用，所以放在setUpClass
		cls.token = handler.token
		cls.member_id = handler.member_id

	def setUp(self) -> None:
		self.db = handler.DbHandler()

	def tearDown(self) -> None:
		self.db.close()

	@ddt.data(*test_data)
	def test_recharge(self,test_info):

		# 替换数据
		data = test_info["data"]
		if "#member_id#" in data:
			data = data.replace("#member_id#", str(self.member_id))

		headers = test_info["headers"]
		if "#token#" in headers:
			headers = headers.replace("#token#", self.token)

		sql_code = test_info["sql_code"]
		if "#member_id#" in sql_code:
			sql_code = sql_code.replace("#member_id#",str(self.member_id))

		# 数据库数据获取
		user_info = self.db.query(sql_code)
		before_amount = user_info[0]['leave_amount']
		# print(before_amount)

		# 访问接口
		res = requests_handler.visit(
			url=handler.yaml["host"]+test_info["url"],
			method= test_info["method"],
			headers=json.loads(headers),
			json = json.loads(data)  # data不满足json格式时会报错
		)

		# 断言
		expected = json.loads(test_info["expected"])
		self.assertEqual(expected["code"], res["code"])
		self.assertEqual(expected["msg"], res["msg"])

		# 数据库校验
		if res["code"] == 0:
			self.db.conn.commit()  # 提交事务
			user_info_after = self.db.query(sql_code)
			after_amount = user_info_after[0]['leave_amount']
			print(after_amount)
			self.assertTrue(before_amount+Decimal(str(json.loads(data)["amount"])) == after_amount)
