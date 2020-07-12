import openpyxl


class ExcelHandler(object):
	def __init__(self,file_path):
		self.file_path = file_path
		self.workbook = None

	def open_file(self):
		"""打开excel，返回workbook"""
		workbook = openpyxl.load_workbook(self.file_path)
		self.workbook = workbook
		return workbook

	def get_sheet(self,sheet_name):
		"""根据工作表名返回文件file_path的sheet"""
		workbook = self.open_file()
		# print("获取表格%s"%sheet_name)
		return workbook[sheet_name]

	def read_data(self,sheet_name):
		"""以字典元素的列表返回指定工作表中的数据"""
		# print("读取%s中%s中的数据"%(self.file_path,sheet_name))
		sheet = self.get_sheet(sheet_name)
		row_generator = sheet.rows

		test_data_dlist = []
		key_list = []
		for i, item in enumerate(row_generator):  # 遍历每行数据的元组
			if i == 0:  # 获取第一行取成字典元素的key列表
				for key_item in list(item):
					key_list.append(key_item.value)
			else:  # 根据key列表和后续行的数据组成一个字典，并把字典添加到数据列表里
				line_data = {}  # 用于接收数据构成数据列表中的字典元素
				for key, cell_data in zip(key_list, list(item)):
					line_data[key] = cell_data.value
				test_data_dlist.append(line_data)
		# print("————读取%s中的%s中的数据成功" % (self.file_path, sheet_name))
		return test_data_dlist

	def write_in_sheet(self,sheet_name):
		"""向sheet_name中写入数据"""
		sheet = self.get_sheet(sheet_name)

		def write_data(row,column,data):
			"""向第row行column列数据data"""
			sheet.cell(row=row,column=column).value=data
			self.workbook.save(self.file_path)
		return write_data

	def save(self):
		self.workbook.save()

	def close(self):
		# print("关闭文件：%s"%self.file_path)
		self.workbook.close()


if __name__ == '__main__':

	print(ExcelHandler("test_cases_data.xlsx").read_data("login"))
	# list = []
	# for k,v in zip([1,2,3],[4,5,6]):
	# 	print(k,v)
	# 	list.append((k,v))
	# print(list)
	handler = ExcelHandler("test_cases_data.xlsx")
	handler.read_data("login")
	write = handler.write_in_sheet("login")
	# write(2,11, None)

