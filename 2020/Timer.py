import time

def timer(func):

	def wrapper(*args):
		t = time.perf_counter()
		res = func(*args)
		print(func.__name__, time.perf_counter()-t)
		return res

	return wrapper
