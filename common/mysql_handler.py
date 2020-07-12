import pymysql
from pymysql.cursors import DictCursor


# 结构：instance(conn,cursor,query(),close())
class MySQLHandler(object):
	# 配置文件
	def __init__(self,
				 host=None,
				 port=3306,
				 user=None,
				 password=None,
				 charset='utf8',
				 cursorclass=DictCursor
				 ):
		self.conn = pymysql.connect(
			host=host,
			port=port,
			user=user,
			password=password,
			charset=charset,
			cursorclass=cursorclass
		)
		self.cursor = self.conn.cursor()
	def query(self, sql, one=False):
		self.conn.commit()
		self.cursor.execute(sql)
		if one:
			return self.cursor.fetchone()
		return self.cursor.fetchall()

	def close(self):
		self.cursor.close()
		self.conn.close()


if __name__ == '__main__':
	dbh = MySQLHandler(
		host='120.78.128.25',
		port=3306,
		user='future',
		password='123456',
		charset='utf8',  # 不能使utf-8
		# database = 'future',
		cursorclass=DictCursor  # 设置游标返回的数据类型为字典
	)
	print(dbh)
	data = dbh.query('SELECT * FROM futureloan.member LIMIT 10;')
	print(data)
