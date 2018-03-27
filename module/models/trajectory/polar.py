from .base import Trajectory
import numpy as np

class PolarTrajectory(Trajectory):
    """
    Mathematical model of a polar trajectory
    """
    def disposition(self,t) -> np.ndarray:
        print("Polar") 
        
