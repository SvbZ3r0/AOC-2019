import time

def timer(func):

	def wrapper(*args):
		t = time.clock()
		res = func(*args)
		print(func.__name__, time.clock()-t)
		return res

	return wrapper
