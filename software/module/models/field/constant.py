from .base import Field
import numpy as np

from ..physics.electricity import μ0

class ConstantField(Field):
    """
    The mathematical model of a tangential field.
    """
    def __init__(self, vec):
        """
        Initializes the field
        """
        self.vec = vec

    def field(self, vec) -> np.ndarray:
        """
        vec3 - [angle - radians,
                height (above center of planet) - meters
        ]
        """

        # Field magnitude: STRENGTH*Mu0/R^2
        return np.array(self.vec)