from abc import ABC, abstractmethod
import numpy as np

class Field(ABC):
    """
    Abstract class to represent a magnetic field.
    """
    @abstractmethod
    def disposition(self, vec3) -> np.ndarray:
        pass
