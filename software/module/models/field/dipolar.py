from .base import Field
import numpy as np
import math

from ..physics.electricity import μ0

class DipolarField2D(Field):
    """
    The mathematical model of a Dipole based field.
    """
    def __init__(self, moment):
        self.moment = moment

    def field(self, vec2) -> np.ndarray:
        angle = math.radians(vec2[0])
        c = math.cos(angle)
        s = math.sin(angle)
        m = length(self.moment)
        return numpy.array([
        3 * c * s,
        3 * c ** 2 - 1
        ]) * m * μ0 / vec2[1] ** 3

    def length(vec):
        return math.sqrt(sum(vec))
