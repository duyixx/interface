import requests


def visit(url,method="GET",**kwargs):
	# 返回访问的网址的响应体
	res = requests.request(method.lower(),url,**kwargs)
	try:
		return res.json()
	except Exception as JsonError:
		print("返回数据不是json格式,url:{}".format(JsonError))
		raise JsonError
		return None


if __name__ == '__main__':
	print(visit("http://www.baidu.com","post"))

