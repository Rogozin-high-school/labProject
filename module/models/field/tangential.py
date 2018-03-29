from .base import field
import numpy as np

class TangentialField(Field):
    """
    The mathematical model of a tangential field.
    """
    def disposition(self, vec3) -> np.ndarray:
         print("Circular")
		if(vec3[1] == 0):
			#handles 2D circular field
			angle = vec3[0]
			size = vec3[2]
			a = math.sin(angle)
			b = math.cos(angle)
			if(b > __MIN_SIZE__ or b < - __MIN_SIZE__):
				x = 1 * (b / abs(b))
				y = -a / b
				length = math.sqrt(x**2 + y**2)
				x = (x / length) * size
				y = (y / length) * size
				return np.ndarray([x,y])
			else:
				x = 0
				y = -a * size
				return numpy.ndarray([x,y])