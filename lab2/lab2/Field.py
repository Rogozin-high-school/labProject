import numpy
import math

def circular_field(angle:float)->numpy.ndarray:
	angle = math.degrees(angle)
	l = 1
	a = math.sqrt(1 / math.cos(angle)**2 - 1)
	x = math.sqrt(a**2 / (1 + a**2))
	y = math.sqrt(1 / 1 + a**2)
	return numpy.ndarray([x,y,0])