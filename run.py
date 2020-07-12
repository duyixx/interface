import os
import unittest
import datetime
from config import config
from libs.HTMLTestRunnerNew import *
import tests.test_audit

# 加载用例
loader = unittest.TestLoader()
test_suit = unittest.TestSuite()
test_suit.addTest(loader.loadTestsFromModule(tests.test_audit))

# 测试报告
report_filename = "report-{}.html".format(datetime.datetime.now().strftime(r"%Y-%m-%d-%H-%M-%S"))
report_file = os.path.join(config.REPORT_PATH,report_filename)

# 运行用例
with open(report_file, "wb") as rp:
	runner = HTMLTestRunner(
		rp,
		title="测试报告:审核项目",
		description="描述信息",
		tester="john Smith"
	)
	runner.run(test_suit)
