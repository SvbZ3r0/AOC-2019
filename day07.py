# Amplification Circuit

from itertools import permutations
import threading

from DataGetter import get_data
from Ship import IntcodeComputer
from Timer import timer

DAY = 7

data = get_data(DAY)
# data = '3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0'
# data = '3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0'
# data = '3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0'
# data = '3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5'
# data = '3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10'

data = [i for i in map(int, data.strip('\n').split(','))]

# problem 1 - no feedback loop
phases = (0, 1, 2, 3, 4)

pos_phase_settings = (i for i in permutations(phases))
propogative_feedback = False

@timer
def get_thrust_nfl():
	max_thrust = 0
	amplifier = IntcodeComputer(data, propogative_feedback)
	amplifier.verbose = False
	for setting in pos_phase_settings:
		val = 0
		for phase in setting:
			amplifier.set_memory(phase)
			amplifier.set_memory(val)
			amplifier.compute()
			val = amplifier.retr_memory()
			amplifier.reset()
		max_thrust = max(max_thrust, val)
	return max_thrust

print(get_thrust_nfl())

# problem 2

phases = (5, 6, 7, 8, 9)

pos_phase_settings = (i for i in permutations(phases))
propogative_feedback = True

def amplifier_setup(setting, propogative_feedback):
	amplifiers = []
	for i, phase in enumerate(setting):
		amplifiers.append(IntcodeComputer(data, propogative_feedback))
		amplifiers[i].verbose = False
		amplifiers[i].set_memory(phase)
	amplifiers[0].set_memory(0)
	threads = []
	for amplifier in amplifiers:
		x = threading.Thread(target=amplifier.compute, daemon=True)
		threads.append(x)
	return amplifiers, threads

@timer
def get_thrust_fl():
	max_thrust = 0
	for setting in pos_phase_settings:
		val = 0
		amplifiers, threads = amplifier_setup(setting, propogative_feedback)
		# print(setting)
		for i, thread in enumerate(threads):
			thread.start()
		i = 0
		flag = [0] * 5
		while True:
			if not amplifiers[-1].is_running:
				val = amplifiers[-1].output
				for amplifier in amplifiers:
					if amplifier.is_running:
						amplifier.quit()
					amplifier.reset()
				break
			else:
				val = amplifiers[i].retr_memory()
			i = (i + 1) % 5
			amplifiers[i].set_memory(val)
		# print(val)
		max_thrust = max(max_thrust, val)
	return max_thrust

print(get_thrust_fl())

