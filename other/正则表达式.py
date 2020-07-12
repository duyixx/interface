# coding:utf-8

# 继承关系

#
# class A:
# 	""""""
# 	pass
#
#
# class B(A):
# 	pass
#
#
# class C(A):
# 	pass
#
#
# class D(B, C):
# 	pass
#
#
# d = D()
#
#
# # d.a
# # 新式类找a：D→B→C→A		广度优先，Python3中全是新式类
# # 旧式类找a：D→B→A→C		深度优先，
#
# class Foo(object):
# 	c_pro = 10  # 类属性
#
# 	@classmethod
# 	def c_met(cls):
# 		pass
#
# 	def __init__(self):
# 		self.obj_pro = 11
#
#
# f = Foo()
# print(dir(Foo))  # 查看对象由哪些属性
# print(Foo.__dict__)
# print(f.__dict__)
# # 类属性、实例属性以键值对的形式被放到类、对象的__dict__方法中
# # 成员查找时会先查找对象的再查找上级类的成员
# f.__setattr__("fs", 56)
# print(f.fs)
# print(f.__getattribute__("fs"))
#
# # __getattr__()：使用对象调用成员在__dict__()中找不到时会调用这个方法
#
# # __getattribute__()：使用 self.xxx 时，实际上是调用__getattribute__去查找xxx
#
# # 正则表达式：描述文本格式
# # re模块：

import re

parttern = r"xxx"
s = "xxxx"
result = re.match(parttern, s)
print(result)
# todo 正则表达式
"""正则表达式：表示字符"""
# . 匹配任意1个字符除了\n
# 匹配[]中列举的字符
# \d 匹配数字，					即[0-9]
# \D 匹配非数字					即[^0-9]
# \s 空白，即tab键、空格键
# \S 非空白[]
# \w 单词字符a-z，A-Z，0-9，_，	即[a-zA-Z0-9_]
# \W 非单词字符，				即[^a-zA-Z0-9_]

print(re.match(r"\W\w\d", "& e1sdf"))
# 注意 group()要在匹配到内容时才有，否则re.match 返回的是None

"""正则表达式：表示数量"""
# * 	0次到无限次		即{0,}
# + 	1次到无限次		即{1,}
# ? 	0次到1次、非贪婪	即{0,1}
# {m} 	m次
# {m,n}	m到n次
# {m,} 	m次以上

print(re.match(r"\d?\d", "99"))
print(re.match(r"\w*", "()"))  # 从""+"()"中匹配空字符串""
# 原始字符串： r"\wabc"

"""正则表达式：表示边界"""
# ^	匹配字符串的开头	：匹配“开头”后就匹配asd：  r"^asd"
# $ 结尾		：匹配asd后就匹配“结尾”：	r"asd$"
# \b 单词边界		：匹配边界	r"\bsddf\bsdfs\bsdf"  →"sddf sdfs sdf"
# \B 非边界		：匹配非边界
# ————（注意，边界只能为空白（\s）和无，只能匹配单词边界和非边界）
print(re.match(r"as\s\bas\B\Bd\b\s>>a\b", "as asd >>a"))

"""正则表达式：分组"""
# | 	二配一：a|b
# () 	括号内的字符串为一组：和group()连用，可用于把提取出的结果分段提取。也可用于指明一组表达式
# \num	引用前面的分组匹配到的字符串
# <?P<name>表达式> 分组起别名
# <?P=name>			引用指定别名的分组匹配到的字符串

# 分组作用：指定匹配的分段格式来提取指定的部分；表达式分组
# ————————url ：  /book/med/inner  → /(book)/(med)/(inner)
# ————通过分组可以提取字符串中的特定部分
# ————————网页 <html></html>

# 匹配0-100之间的数字
print(re.match(r"^[1-9]\d?|0|100$", "100"))  # 10
print(re.match(r"^100|[1-9]?\d$", "100"))  # 100
# ————————|匹配时要注意前面的满足了就返回了

# .group(num)，返回分组编号为num的字符串
print(re.match("(<html>)(.*)(</html>)", "<html>hahah</html>").group(1))

# \num 引用分组，通过\num引用来匹配指定格式<h1><h2>text<h2><h1>
s = "<h1><h2>hahah</h2></h1>"
print(re.match(r"<(.+)><(.+)>(.+)</\2></\1>", s).group(3))
# \num和名字调用可以通用不冲突
print("分组起别名和引用：", re.match(r"<(?P<key1>.+)><(?P<key2>.+)>(?P<key3>.+)</\2></(?P=key1)>", s).group(3)
	  )

# 匹配邮箱：
parttern1 = r"(\w+)@(163|126|qq|gmail)\.(com|cn|net)$"  # ()起分组效果
print(re.match(parttern1, "121@qq.com").group(1))

# todo re高级用法
# re.search(parttern,s) # 从s中搜索第一个,返回一个re对象
re.search(r"^a", "sdf")  # 搜索以"a"开头的
re.search(r"a", "fsd")  # 搜索"a",与"^a"是不同的

# re.findall(parttern,s)	# 从s中匹配所有，并返回一个列表

# re.sub(parttern,"替换成",s)
print(re.sub(r"\d+", "50", "a=1000,b=1254"))  # 将数字替换为50


# todo:使用函数作为re.sub的第二个参数对匹配到的字符串做更智能的处理
#
def replace(result):
	print(result.group())
	r = 1 if int(result.group()) > 5 else 0
	# return "50"	# 需要return字符串，不然sub会不起效
	return str(r)


print(re.sub(r"\d", replace, "a=1649283755"))  # 字符中数字>5变为1否则变为0

# 提取域名：从url中匹配所有字符并用域名组替换匹配到的所有字符后返回
surl = "https://mbd.baidu.com/newspage/data/landingsuper?context=%7B%22nid%22%3A%22news_10335873909382770143%22%7D&n_type=0&p_from=1"
print("提取域名",
	  re.sub(r"(https://.+?/)(.*)", lambda x: x.group(1), surl))

""" 三引号注释是占用内存的，和#不同，它还是一个字符串"""

# 贪婪模式：默认前匹配贪婪
print(re.match(r"(\d+)(\d+\w)", "112233w").groups())
# 关闭贪婪模式：前面的正则满足后优先安排后方的正则满足
print(re.match(r"(\d+?)(\d+\w)", "112233w").groups())
# 可对 +、*、?、{} 使用?关闭表达式的贪婪模式：尽可能少匹配
print(re.match(r"(\d{0,5}?)(\d{0,5})", "112233w").groups())
print(re.match(r"(\d{0,5})(\d{0,5})", "112233w").groups())

# match		从字符串开头开始匹配，
# search	返回第一个符合匹配的字符串的re对象，
# find_all	返回列表
