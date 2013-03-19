import datetime

def getNowString():
	"""return current time in format as described below"""
	now = datetime.datetime.now()
	return now.strftime("%Y-%m-%d %H:%M")
	
