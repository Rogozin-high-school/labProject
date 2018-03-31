from .base import Trajectory
import numpy as np

class CircularTrajectory2D(Trajectory):
    """
    Mathematical model of a polar trajectory
    """
    def __init__(self, altitude, circle_time):
        """
        Altitude - height above the center of the planet
        """
        self.altitude = altitude
        self.angular_velocity = 360 / circle_time

    def disposition(self, t) -> np.ndarray:
        return np.array([(self.angular_velocity * t) % 360, self.altitude])
        
