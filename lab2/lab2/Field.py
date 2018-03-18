import numpy
import math

FIELD_SIZE = 10

def circular_field(angle:float)->numpy.ndarray:
	angle = math.degrees(angle)
	a = math.sin(angle)
	b = math.cos(angle)
	x = None
	y = None
	if(b!=0):
		x = math.sqrt(10 / ((a**2 / b**2) + 1))
		y = -1 * a * x / b
	else:
		x = 0
		y = a * FIELD_SIZE
	return numpy.ndarray([math.sin(angle),math.cos(angle)])