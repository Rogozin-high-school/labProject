from .base import Field
import numpy as np
import math

from ..physics.electricity import μ0

class DipolarField(Field):
    """
    The mathematical model of a Dipole based field.
    """
    def __init__(self, moment) -> np.ndarray:
        self.moment = moment
	
    
    def field(self, vec):
        """
        vec3 - [angle - radians,
                height (above center of planet) - meters
        ]
        """
        c = math.cos(math.radians(vec[0] + 90))
        s = math.sin(math.radians(vec[0] + 90))
        m = self.moment
        return np.array([
            3 * c * s,
            3 * c ** 2 - 1
        ]) * m  * μ0 / (self.vec[1] ** 3)
