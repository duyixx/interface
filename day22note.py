"""接口文档："""
# URL格式：http://ip:port/futureloan/apiName
# ——————http://120.78.128.25:8766/futureloan/member/register
# 路径信息可以放到配置文件中，因为项目运行过程它是不会变化的。但是不同的项目会有不同的路径
# ————不放到yaml中？yaml中存放静态数据
# ————可以放到一个py模块中

"""json：-->str"""
# json 是一种与语言无关的数据交换的格式，
# ————格式：一个对象用{}表示、一对属性之间用:来分隔；一个数组用[]符号
# ————json格式的字符串用双引号、空为null、布尔值为true、false（全小写）

# json是用按js语言规则写的一种特殊标记的字符串，所以在其他语言中不能直接使用→json模块
# ————#如：d_dict=eval（'"mobile_phone"：true，"pwd"："12345678"，"type"：11'）
# ————在Python中会因为true被识别为引用而报错→需要用json模块来读取json格式的文本

# json模块：
import json

row_data = '{"pwd":"123456","user":"aria","is_student":true}'  # -->json格式的Python-str对象
print(type(row_data), row_data)
# 将json格式的python字符串对象转为Python字典对象：
dict_data = json.loads(row_data)  # -->python-dict对象
print(type(dict_data), dict_data)
# 将Python字典转化为json格式的Python字符串：
json_data = json.dumps(dict_data)  # -->json格式的Python-str对象
print(type(json_data), json_data)

# 总结：loads、dumps：<class 'dict'> dict ↔ <class 'str'> json-str
# ————dumps返回的不是json对象，而是json格式的字符串对象
# ————如果测试数据用json格式来写，加载数据时要用json.loads()来转换格式。
# ————如果接口入参是json格式，request.request(**,json )里json需要接收json字符串，需要用loads()来转换json字符串为字典后传入


"""logger使用："""
# 用途：日志文件用来记录错误和运行日志(info级上)，debug日志一般输出到控制台
# 用法：在关键的信息点记录日志——logger.error()、logger.info()

"""操作MySQL数据库："""
# ————测试注册成功用例需要在数据库进行验证、需要使用数据库没有的注册账号
# 操作数据库需要使用db-api，现在用pymysql:
# ————接口：base_url:http://120.78.128.25:8766/futureloan
# ————MySQL链接信息： 主机 120.78.128.25，port 3306，用户 future ，密码 123456
# ————连接数据库表futureloan.member

import pymysql
import copy

# a.建立连接
conn = pymysql.connect(
	host='120.78.128.25',
	port=3306,
	user='future',
	password='123456',
	charset='utf8',  # 不能使utf-8
	# database = 'future',
	cursorclass=pymysql.cursors.DictCursor  # 设置游标返回的数据类型为字典
)

# b.建立一个游标对象
cursor = conn.cursor()

# c.使用execute()执行sql语句
cursor.execute('SELECT * FROM futureloan.member where mobile_phone = "1" LIMIT 10;')
cursor2 = copy.copy(cursor)


# d.使用fetch进行查询数据：
# ————返回元组元素型元组（（）,（）,...），
# ————或者字典元素型列表[{},{},...]
# cursor.fetchone()		# 返回游标位置后的第一行数据
# cursor.fetchmany(5)		# 游标位置后指定长度数据
# cursor.fetchall()  	# 返回cursor.rownumber后的余下所有数据
# ————如果数据为空，fetch返回一个空元组
# 使用.rownumber操作游标位置：
# cursor.rowcount	# 返回游标队列里数据的总行数(该数值由cursor.execute()时赋值)
# cursor.rownumber		# 返回游标的位置：0，表示下一个fetchone为第一行数据，可以自己设置
# ————重复读取数据？新建游标并执行sql/copy未fetch的对象/设置游标位置rownumber的值

print(cursor.rowcount)
print(cursor.rownumber)
res = cursor.fetchall()
print(res)
print(cursor.rowcount)
print(cursor.rownumber)
cursor.rownumber = 3
cursor.rowcount = 3
print(cursor.rowcount)
print(cursor.rownumber)
res = cursor.fetchmany(5)
print(res)
print(cursor.rowcount)
print(cursor.rownumber)
cursor.execute('SELECT * FROM futureloan.member LIMIT 10;')
print(cursor.rowcount)

# e.关闭
cursor.close()  # 关闭游标，游标不能再执行数据库语句，但仍然是可读的（该对象仍然存在）。
# cursor2.close()
# cursor3.close()
conn.close()

"""参数化"""
# 使用python字符串方法进行参数化

"""数据中间层封装：middler ware"""
# 1. 初始化直接用配置文件
# 2. 封装数据中间层的目的：和项目有关系，不需要重复写大段代码
# 封装内容：config、yaml、logger、excel
# ————每个用例的脚本文件中需要获取使用yaml和config获取用例数据excel、实例化日志生成器对象
# ————使用数据中间层封装这些执行用例前的固定操作，可以简化测试用例脚本的编写
# ————访问数据库的pymysql对象，由于配置参数是固定的，也可以用中间层封装。只不过需
# ——————要多套配置参数时需要额外处理继承为多个MySQLHandlerMid类

"""1. 登录：数据依赖"""
# 登陆的手机号和密码可以提前准备好，直接放到yaml配置文件中；或者放到Excel文件中用#mobile#、#pwd# 标识
# 因为很多用例都共用，可封装到中间层→Handler
# 对需要提取的依赖数据，可以用@property装饰成实例属性方便用Handler()调用
# （要注意这些数据是否是对应变动的，如token和tokenid对应，则不能分开获取）
"""@property装饰：方法→实例属性"""

"""2. 充值接口"""
# 需要用到member_id，可以直接放到yaml中（和账号一样），也可以放到excel中用#member_id# 标识
# 接口依赖：不同接口调用时需要之前接口返回的信息。可以用jsonpath提取
# 如果是高复用的，可以考虑将获取的过程封装到middleware
# ————————充值接口：1，获取token，2，获取member_id

"""接口拼接"""
# 不同环境、项目有不同的域名和端口：
# 将域名和端口放在yml配置文件或者py配置文件，将用例执行的地址放在excel中，使用handler拼接
# 拼接接口

"""jsonpath"""
# $ 根节点
# . 子节点
# .. 子孙节点
# 匹配结果以列表形式返回，无匹配结果则返回False
import jsonpath
user = {"a":{"b2":2},"b":{"b":3}}
print(jsonpath.jsonpath(user,"$.a"))
print(jsonpath.jsonpath(user,"$..b"))

"""decimal.Decimal"""
# 浮点数精度运算：
# decimal.Decimal("0.1")+decimal.Decimal("0.2") == decimal.Decimal("0.3") is True
# 要注意数据库中查询出来的数据的类型

"""3.添加项目"""
"""4.审核项目"""
# 1.普通用户登录：新建项目
# 1.管理员登录：审核项目
# 2.loan/add，添加项目，（没有审核）
# 3.审核 成功判断
# ————预期结果：status=2
# ————loan 表 的status
# 4.用例之间可能具有依赖性（如用第一个用例生成的数据执行第二个用例），可以
# ————用临时变量在不同用例间传递数据或者直接查询数据库获取数据

"""多数据替换？利用正则表达式"""
# 正则表达式的作用：匹配
# 接口自动化的难点：动态数据（参数化）和前置条件（接口依赖）
import re
pattern = r'#(.*?)#'
rp = re.sub(pattern,'123','{"username":"#user#","pwd":"#pwd#",#so#}',2)


def replace_data(self, data):
	import re
	pattern = r"#(.*?)#"
	while re.search(pattern, data):
		key = re.search(pattern, data).group(1)
		value = getattr(self, key, "")
		data = re.sub(pattern, str(value), data, 1)
	return data

"""投资用例、Jenkins集成、mock测试"""
# 自动化是解决一些成本低的用例执行问题。对于复杂度高的用例自动化成本高的话不如手工测试
# jenkins继承
# mock

## Jenkins 安装
# - war包安装、可执行文件安装、容器安装等等

# - war包安装启动：java -jar jenkins.war --httpPort=8080
# - 可执行文件安装后启动：jenkins配置文件：jenkins.xml，配置后需要重启服务

# 创建项目-配置-构建
# 报告插件：HTML Publisher.plugin
# 离线下载：plugins.jenkins.io
# 发送邮件：Email Extension Plugin

# mock测什
# 模拟数据进行测试，而不是使用接口真正返回的数据
# - 1. 接口未完成，只能自己模拟数据出来
# - 2. 第三方的不方便直接调用的接口。如支付接口。（模拟数据返回而调试代码）
