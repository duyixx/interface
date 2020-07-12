import os
import time
import unittest
import ddt
import json

from common.excel_handler import ExcelHandler
from config import config
from common import requests_handler, yaml_handler, logging_handler

# 读取yaml配置文件
yaml_data = yaml_handler.read_yaml(os.path.join(config.CONFIG_PATH, "config.yml"))

# 读取logger配置文件并初始化logger
logger_config = yaml_data["logger"]
logger = logging_handler.LoggerHandler(
	logger_name=logger_config["logger_name"],
	logger_level=logger_config["logger_level"],
	file_name=os.path.join(config.LOG_PATH, logger_config["file_name"]),
	file_level=logger_config["file_level"],
	stream_level=logger_config["stream_level"],
	fmt='%(asctime)s-%(filename)s-->line:%(lineno)d-%(levelname)s:%(message)s'
)

# 读取test_cases.xlsx里login表单的数据
logger.info("读取数据:")
cases_file = yaml_data["excel"]["test_datafile"]
xls = ExcelHandler(os.path.join(config.DATA_PATH, cases_file))
test_data = xls.read_data("login")
logger.info("读取数据成功,测试数据为:{}".format(test_data))
time.sleep(1)


@ddt.ddt
class TestLogin(unittest.TestCase):
	"""测试登录接口"""
	@classmethod
	def setUpClass(cls):
		logger.info("执行登录接口的测试用例")

	@classmethod
	def tearDownClass(cls):
		logger.info("测试登录接口结束")

	@ddt.data(*test_data)
	def test_login(self, test_info):
		print(test_info)
		# 访问接口
		res = requests_handler.visit(
			url=test_info["url"], method=test_info["method"],
			headers=json.loads(test_info["headers"]), json=json.loads(test_info["data"])
			# 形参json、headers入参要用字符串
		)
		# 获取期望
		expected_data = json.loads(test_info["expected"])
		# print(expected_data)

		# # 断言
		# self.assertEqual(
		# 	eval(test_info["expected"]["msg"]),
		# 	res["msg"]
		# )
		for k, v in expected_data.items():
			try:
				self.assertEqual(v, res[k])
				logger.info("用例执行通过:{}，{}正确".format(
					__name__ + ":" + test_info["title"], k))
			except AssertionError as e:
				logger.error("用例执行未通过{}：{}".format(
					__name__ + ":" + test_info["title"], e))
				raise e
