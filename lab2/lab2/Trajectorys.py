from abc import ABC, abstractmethod
import numpy as np

class Trajectory(ABC):
    #t means the time that pass from the start time
    @abstractmethod
    def disposition(self,t) -> np.ndarray:
        pass
        
class PolarTrajectory(Trajectory):
    
    def disposition(self,t) -> np.ndarray:
        print("Polar") 

class GeocentricTrajectory(Trajectory):

    def disposition(self,t) -> np.ndarray:
        print("Geocentric")