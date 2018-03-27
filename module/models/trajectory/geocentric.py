from .base import Trajectory
import numpy as np

class GeocentricTrajectory(Trajectory):
    """
    Mathematical model of a polar trajectory
    """
    def disposition(self,t) -> np.ndarray:
        print("Geocentric")