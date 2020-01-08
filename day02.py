# 1202 Program Alarm

from DataGetter import get_data
from Ship import IntcodeComputer
from Timer import timer

DAY = 2

data = get_data(DAY)
data = [i for i in map(int, data.strip('\n').split(','))]

def _comp(comp, noun, verb):
	comp.overwrite_intr(noun, 1)
	comp.overwrite_intr(verb, 2)
	comp.compute()
	val = comp.retr_intr(0)
	comp.reset()
	return val

@timer
def compute(*args):
	return _comp(*args)

@timer
def gravity_assist(comp, output):
	for noun in range(100):
		for verb in range(100):
			if _comp(comp, noun, verb) == output:
				val = (noun * 100) + verb
				return val
	print('Unable to compute for {}'.format(output))

comp = IntcodeComputer(data)
comp.verbose = False
output = 19690720

# problem 1
print(compute(comp, 12, 2))

# problem 2
print(gravity_assist(comp, output))