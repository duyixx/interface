import unittest
import random

import ddt
import json
import pymysql

from common.mysql_handler import MySQLHandler
from common import requests_handler
from middlerware.handler import Handler


# 实例化中间数据层handler
handler = Handler()
# 使用handler初始化logger
logger = handler.logger
# 使用handler加载测试数据
test_data = handler.xls.read_data("register")

@ddt.ddt
class TestResgister(unittest.TestCase):
	"""测试注册接口"""

	@ddt.data(*test_data)
	def test_register(self, test_info):
		# print(test_info)

		# 动态设置入参为不重复的手机号
		if "#phone#" in test_info["data"]:
			replace_phone = self.random_dis_phone()
			test_info["data"] = test_info["data"].replace("#phone#", replace_phone)
		logger.info("用例id：{}—测试数据为：{}".format(test_info["case_id"], test_info["data"]))

		# 访问接口
		res = requests_handler.visit(
			url=test_info["url"], method=test_info["method"],
			headers=json.loads(test_info["headers"]), json=json.loads(test_info["data"])
			# 形参json、headers入参要用字符串字符串
		)

		# 断言
		expected_data = json.loads(test_info["expected"])  # 用例期望
		expected_data_phone = json.loads(test_info["data"])["mobile_phone"]  # 执行用例使用的手机号
		for k, v in expected_data.items():
			try:
				self.assertEqual(v, res[k])
				logger.info("{}：用例id：{}执行通过：{}正确".format(
					__name__, test_info["case_id"], k))
				# 如果注册成功，需要从数据库进行验证
				if res["code"] == 0:
					check_sql = "SELECT * FROM futureloan.member WHERE mobile_phone = {} LIMIT 1;".format(expected_data_phone)
					check_db = handler.DbHandler()
					self.assertTrue(check_db.query(check_sql) != ())
					logger.info("用例id：{}—数据库验证手机号通过：{}".format(test_info["case_id"], expected_data_phone))
			except AssertionError as e:
				logger.error("测试用例未通过:{}".format(e))
				raise e

	def random_dis_phone(self):
		"""随机生成一个动态的手机号
		需要的是数据库用户表里没有的"""
		while True:  # 生成号码，查表看是否重复，不重复则返回否则循环
			distinct_phone = "1" + random.choice(["3", "5", "7", "8", "9"])
			for i in range(9):
				distinct_phone += str(random.randint(0, 9))
			db = handler.DbHandler()
			phone_recode = db.query(
				"select * FROM futureloan.member WHERE mobile_phone = {} LIMIT 1".format(distinct_phone), True)
			if not phone_recode:
				db.close()
				return distinct_phone



