import numpy
import math

def circular_field(angle):
	angle = math.radians(angle)
	a = 1
	b = -a / (1/math.cos(angle)**2 -1)
	return numpy.array([a,b])
	