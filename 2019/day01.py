# The Tyranny of the Rocket Equation

from DataGetter import get_data
from Timer import timer

DAY = 1

data = get_data(DAY)
data = [i for i in map(int, data.strip('\n').split('\n'))]

def calc_fuel(mass, recr=True):
	c_fuel = lambda m: (m // 3) - 2 if m > 8 else 0
	fuel = c_fuel(mass)
	if not recr or fuel == 0:
		return fuel
	else:
		return fuel + calc_fuel(fuel, recr)

# problem 1
@timer
def calculate_fuel(data):
	total_fuel = sum([i for i in map(lambda x: calc_fuel(x, False), data)])
	return total_fuel

print(calculate_fuel(data))

# problem 2
@timer
def calculate_fuel_recursive(data):
	total_fuel = sum([i for i in map(calc_fuel, data)])
	return total_fuel

print(calculate_fuel_recursive(data))