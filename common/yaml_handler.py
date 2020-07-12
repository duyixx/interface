import yaml


def read_yaml(file):
	"""读取 yaml"""
	with open(file,encoding="utf-8") as f:
		conf = yaml.load(f, Loader=yaml.SafeLoader)
		return conf

def write_yaml(file,data):
	"""写入"""
	with open(file,data) as f:
		yaml.dump(data,f)
