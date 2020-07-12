import unittest
import random

import ddt
import json
from decimal import Decimal

from common import requests_handler
from middlerware.handler import Handler

# 加载数据
handler = Handler()
test_data = handler.xls.read_data("withdraw")
# 用于写入用例执行结果
result_write = handler.xls.write_in_sheet("withdraw")
# 初始化日志
logger = handler.logger


@ddt.ddt
class TestWithdraw(unittest.TestCase):

	@classmethod
	def setUpClass(cls) -> None:
		# 登录
		cls.token = handler.token
		cls.member_id = handler.member_id
		logger.info("登录成功，member_id为：{}。开始执行提现接口的用例".format(cls.member_id))

	@classmethod
	def tearDownClass(cls) -> None:
		logger.info("提现接口用例执行结束")

	def setUp(self) -> None:
		self.db = handler.DbHandler()


	def tearDown(self) -> None:
		self.db.close()


	@ddt.data(*test_data)
	def test_withdraw(self, test_info):
		cid = test_info["case_id"]
		ctl = test_info["title"]
		logger.info("执行用例：id: {}，title: {}".format(cid, ctl))
		result_write(cid+1,10,"此用例执行失败")  # 如果断言没有发生，则用例执行失败，为无效测试

		# 替换数据
		data = test_info["data"]
		if "#member_id#" in data:
			data = data.replace("#member_id#", str(self.member_id))

		headers = test_info["headers"]
		if "#token#" in headers:
			headers = headers.replace("#token#", self.token)

		sql_code = test_info["sql_code"]
		if "#member_id#" in sql_code:
			sql_code = sql_code.replace("#member_id#", str(self.member_id))
		logger.info("数据处理成功")

		# 数据库数据获取
		user_info = self.db.query(sql_code)
		before_amount = user_info[0]['leave_amount']  # :返回的是Decimal类型

		# 访问接口
		res = requests_handler.visit(
			url=handler.yaml["host"] + test_info["url"],
			method=test_info["method"],
			headers=json.loads(headers),
			json=json.loads(data)  # data不满足json格式时会报错
		)
		logger.info("请求发送成功")

		# 过滤前置条件不足的场景
		if res["code"] == 1002:
			logger.error("id:{}执行失败，前置条件不足".format(cid))
			try:
				self.assert_(1 != 1, "id:{}前置条件不足：余额不足".format(cid))
			except AssertionError as e:
				result_write(cid+1,10,"Fail：前置条件不足")
				raise e
		# 断言
		expected = json.loads(test_info["expected"])
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
			self.db.conn.commit()  # 提交事务
			user_info_after = self.db.query(sql_code)
			after_amount = user_info_after[0]['leave_amount']
			self.assertTrue(before_amount - Decimal(str(json.loads(data)["amount"])) == after_amount, "提现后的余额不符合预期")
			logger.info("id:{}，title:{}，PASS。数据库校验通过".format(cid,ctl))
		else:
			logger.info("id:{}，title:{}，PASS".format(cid,ctl))
		result_write(cid+1,10,"Pass")

