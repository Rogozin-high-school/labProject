from abc import ABC, abstractmethod
import numpy as np

class field(ABC):
    
    @abstractmethod
    def disposition(self,vec3) -> np.ndarray:
        pass
        
class dipole_field(field):
    
    def disposition(self,vec3) -> np.ndarray:
        print("dipole") 

class circular_field(field):

    def disposition(self,vec3) -> np.ndarray:
        print("circular")
