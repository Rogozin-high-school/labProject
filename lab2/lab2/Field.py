import numpy
import math

def circular_field(angle:float)->numpy.ndarray:
	angle = math.degrees(angle)
	return numpy.ndarray([math.sin(angle),math.cos(angle)])