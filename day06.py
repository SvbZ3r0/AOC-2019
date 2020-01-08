# Universal Orbit Map

from DataGetter import get_data
from Space import SpaceObj
from Timer import timer

DAY = 6

data = get_data(DAY)
objs = data.strip('\n').split('\n')

COM = SpaceObj('COM')

@timer
def load_starmap(COM, data):
	space_objects = {'COM': COM}
	for pair in objs:
		centre_name, orbitor_name = pair.split(')')
		if centre_name not in space_objects:
			space_objects[centre_name] = SpaceObj(centre_name)
		centre = space_objects[centre_name]
		if orbitor_name in space_objects:
			space_objects[orbitor_name].set_parent(centre)
		else:
			space_objects[orbitor_name] = SpaceObj(orbitor_name, centre)

@timer
def calc_chksm(COM):
	return COM.orbit_count_checksum()

@timer
def get_dist(COM, a, b):
	return COM.get_child_by_name(a).get_dist_from(COM.get_child_by_name(b), True) - 1

load_starmap(COM, data)

# problem 1
print(calc_chksm(COM))

# problem 2
print(get_dist(COM, 'YOU', 'SAN'))