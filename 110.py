import requests

# res = requests.request("get",'http://www.baidu.com',)
# print(res)
# print(res.text)
# sd ="ssdsd"
# sd1 = sd.replace("ss","aa")
# print(sd)
# print(sd1)

# s = '{"member_id":"sdf","amount":600}'
# import json
# print(json.loads(s))
# a = 5
# if a==5:
# 	raise Exception("sdf")
# print(a)
def func(a,b):
	return a+b

def is_fail_assert(exe_string,a,b):
	try:
		eval(exe_string)
	except Exception as e:
		print(func(a,b))
		raise e

is_fail_assert("{}.append(1)",3,4)
