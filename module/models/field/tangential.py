from .base import Field
import numpy as np

class TangentialField(Field):
    """
    The mathematical model of a tangential field.
    """
    def disposition(self, vec3) -> np.ndarray:
        print("Circular")