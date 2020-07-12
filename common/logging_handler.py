# todo：log封装
import logging


# 封装成函数
# def get_logger(
# 		name=None,
# 		logger_level="DEBUG",
# 		stream_level="DEBUG",
# 		filename=None,
# 		file_level="WARNING",
# 		fmt='%(asctime)s-%(filename)s-->line:%(lineno)d-%(levelname)s:%(message)s',
# ):
#
# 	"""获取收集器"""
# 	logger = logging.getLogger()
# 	logger.setLevel(logger_level)
#
# 	"""日志格式"""
# 	formatter = logging.Formatter(fmt)
#
# 	"""输出器.控制台"""
# 	stream_handler = logging.StreamHandler()
# 	stream_handler.setLevel(stream_level)
# 	stream_handler.setFormatter(formatter)
# 	logger.addHandler(stream_handler)
#
# 	"""输出器.文件"""
# 	if filename:
# 		file_handler = logging.FileHandler(filename,"a",encoding="utf-8")
# 		file_handler.setFormatter(formatter)
# 		file_handler.setLevel(file_level)
# 		logger.addHandler(file_handler)
#
# 	return logger
#
# if __name__ == '__main__':
# 	logger =get_logger(filename="log.txt")
# 	logger.info("")
# 	logger.warning("")
# 	logger.error("")


class LoggerHandler(logging.Logger):
	def __init__(self,
				 logger_name=None,
				 logger_level="INFO",
				 file_name=None,
				 file_level="INFO",
				 stream_level="INFO",
				 fmt='%(asctime)s-%(filename)s-->line:%(lineno)d-%(levelname)s:%(message)s'
				 ):
		super().__init__(logger_name, logger_level)
		# 日志格式
		formatter = logging.Formatter(fmt)
		# 输出器.控制台
		stream_handler = logging.StreamHandler()
		stream_handler.setLevel(stream_level)
		stream_handler.setFormatter(formatter)
		self.addHandler(stream_handler)

		# 输出器.文件日志
		if file_name:
			file_handler = logging.FileHandler(file_name, "a", encoding="utf-8")
			file_handler.setFormatter(formatter)
			file_handler.setLevel(file_level)
			self.addHandler(file_handler)

if __name__ == '__main__':
	loger2 = LoggerHandler()
	loger2.error("aaaa")
