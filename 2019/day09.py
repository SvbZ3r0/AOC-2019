# Amplification Circuit

from DataGetter import get_data
from Ship import IntcodeComputer
from Timer import timer

DAY = 9

data = get_data(DAY)
# data = '109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99'
# data = '1102,34915192,34915192,7,4,7,99,0'
# data = '104,1125899906842624,99'
# data = '109,-1,204,1,99'
# data = '109,1,209,-1,204,-106,99'
# data = '109,1,109,9,204,-6,99'

data = [i for i in map(int, data.strip('\n').split(','))]

BOOST_comp = IntcodeComputer(data)

@timer
def compute(val):
	BOOST_comp.set_memory(val)
	BOOST_comp.compute()
	while not BOOST_comp.memory_empty():
		print(BOOST_comp.retr_memory())
	BOOST_comp.reset()

# problem 1
compute(1)

# problem 2
compute(2)