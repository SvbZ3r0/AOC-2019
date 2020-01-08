# Crossed Wires

from DataGetter import get_data
from Timer import timer

DAY = 3

data = get_data(DAY)
data = data.strip('\n').split('\n')
# data[0] = 'R75,D30,R83,U83,L12,D49,R71,U7,L72'
# data[1] = 'U62,R66,U55,R34,D71,R55,D58,R83'
data[0] = [i for i in data[0].split(',')]
data[1] = [i for i in data[1].split(',')]

def traverse(path, curr, dest):
	dirc = dest[0]
	dist = int(dest[1:])
	if dirc == 'R':
		axis = 0
		step = 1
	elif dirc == 'L':
		axis = 0
		step = -1
	elif dirc == 'U':
		axis = 1
		step = 1
	elif dirc == 'D':
		axis = 1
		step = -1
	for i in range(dist):
		curr[axis] += step
		path.append(','.join([str(i) for i in curr]))
	return path, curr

def manhattan_dist(loc_):
	loc = loc_.split(',')
	return abs(int(loc[0])) + abs(int(loc[1]))

@timer
def find_intersections(data):
	curr = [[0, 0], [0, 0]]
	path = [[], []]
	path_set = [[], []]
	for wire in range(len(data)):
		for dest in data[wire]:
			path[wire], curr[wire] = traverse(path[wire], curr[wire], dest)
		path_set[wire] = set(path[wire])

	intersections = list(path_set[0].intersection(path_set[1]))
	return intersections, path

@timer
def manhattan_closest_intersection(intersections):
	m_dists = [i for i in map(manhattan_dist, intersections)]
	return min(m_dists)

@timer
def route_closest_intersection(intersections, path):
	route = []
	for loc in intersections:
		route.append(path[0].index(loc) + 1  + path[1].index(loc) + 1)
	return min(route)

intersections, path = find_intersections(data)

# problem 1
print(manhattan_closest_intersection(intersections))

# problem 2
print(route_closest_intersection(intersections, path))