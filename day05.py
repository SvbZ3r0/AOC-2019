# Sunny with a Chance of Asteroids

from DataGetter import get_data
from Ship import IntcodeComputer
from Timer import timer

DAY = 5

data = get_data(DAY)
data = [i for i in map(int, data.strip('\n').split(','))]

TEST_comp = IntcodeComputer(data)

# problem 1 - ID: 1
# problem 2 - ID: 5
@timer
def compute(val):
	try:
		val = int(val)
	except ValueError:
		print('{} is not a valid integer.'.format(val))
		exit(1)
	TEST_comp.set_memory(val)
	TEST_comp.compute()
	while not TEST_comp.memory_empty():
		print(TEST_comp.retr_memory())
	TEST_comp.reset()

val = int(input('ID:'))
compute(val)