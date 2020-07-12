import os

# 配置文件路径
CONFIG_PATH = os.path.dirname(os.path.abspath(__file__))

# 项目路径
ROOT_PATH = os.path.dirname(CONFIG_PATH)

# 用例路径
CASE_PATH = os.path.join(ROOT_PATH,"tests")

# 测试报告路径
REPORT_PATH = os.path.join(ROOT_PATH,"reports")

# 测试数据路劲
DATA_PATH = os.path.join(ROOT_PATH,"data")

# log日志文件路劲
LOG_PATH = os.path.join(ROOT_PATH,"logs")