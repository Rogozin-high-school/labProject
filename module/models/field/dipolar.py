from .base import Field
import numpy as np

class DipolarField(Field):
    """
    The mathematical model of a Dipole based field.
    """
    def field(self, vec3) -> np.ndarray:
        print("Dipole") 
