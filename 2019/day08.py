# Space Image Format

import numpy as np
from PIL import Image

from DataGetter import get_data
from Timer import timer

DAY = 8

data = get_data(DAY)

# problem 1
@timer
def calc_chksm(data):
	image = np.array([int(i) for i in list(data.strip('\n'))]).reshape((-1,6,25))
	n_0s = []
	for layer in image:
		n_0s.append(np.count_nonzero(layer==0))

	i = n_0s.index(min(n_0s))
	layer = image[i]
	chksm = np.count_nonzero(layer==1) * np.count_nonzero(layer==2)
	return chksm

print(calc_chksm(data))

# problem 2
def colorize(x, y):
	if x == 2: x = y
	return x

@timer
def regenerate_image(data):
	image = np.array([int(i) for i in list(data.strip('\n'))]).reshape((-1,6,25))
	np_colorize = np.frompyfunc(colorize, 2, 1)
	colorized_img = np.uint8(np_colorize.reduce(image) * 255)
	np.set_printoptions(formatter={'all':lambda x: u'\u2591' if x==0 else u'\u2588'})
	# np.set_printoptions(formatter={'all':lambda x: ' ' if x==0 else '#'})
	print(colorized_img)
	pic = Image.fromarray(colorized_img, 'L').resize((800, 192))
	# pic.show()
	pic.save('./img/day8.png','PNG')

regenerate_image(data)