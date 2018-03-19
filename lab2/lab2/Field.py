import numpy
import math
import time
FIELD_SIZE = 10

def circular_field(angle:float)->numpy.ndarray:
	angle = math.radians(angle)
	a = math.sin(angle)
	b = math.cos(angle)
	x = None
	y = None
	if(b!=0):
		x = 1
		y = -a/b
		arr = numpy.ndarray([x,y])
		arr.reize(1)
		return [arr[0],arr[1]]
	else:
		print("\n\n\n")
		x = 0
		y = a * FIELD_SIZE
	return [x,y]


for i in range(0,360,10):
	time.sleep(0.1)
	B = circular_field(i)
	print(str(i)+"-> "+str(B[0])+":"+str(B[1]))