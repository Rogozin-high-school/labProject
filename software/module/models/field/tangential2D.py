from .base import Field
import numpy as np

from ..physics.electricity import μ0

class TangentialField2D(Field):
    """
    The mathematical model of a tangential field.
    """
    def __init__(self, strength):
        """
        Initializes the field
        """
        self.strength = strength

    def field(self, vec) -> np.ndarray:
        """
        vec3 - [angle - radians,
                height (above center of planet) - meters
        ]
        """

        # Field magnitude: STRENGTH*Mu0/R^2
        return np.array([
            np.cos(np.radians(vec[0] + 90)), 
            np.sin(np.radians(vec[0] + 90))
        ]) * (μ0 * self.strength) / (vec[1] * vec[1])