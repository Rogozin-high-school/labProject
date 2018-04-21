import cv2
import numpy as np

from module.models.trajectory.circular2D import CircularTrajectory2D
from module.models.field.tangential2D import TangentialField2D

import module.compass.compass as compass

import time
import os

class Display(object):
    """
    Display unit for the simulation system.
    """
    def __init__(self, _name):
        """
        Creates a new board
        """
        self.screen = np.zeros((600, 800, 3), np.uint8)
        self.display = cv2.namedWindow(_name)
        self.name = _name
        self.renderers = []

    def add_render(self, renderer):
        """
        Adds a renderer to the rendeders list. 
        Every renderer can add or remove elements from the board before it's 
        shown to the user.
        """
        self.renderers.append(renderer)

    def render(self):
        """
        Updates the board and shows it on screen.
        """
        self.screen.fill(255)
        for r in self.renderers:
            self.screen = r(self.screen) or self.screen
        cv2.imshow(self.name, self.screen)

    def __del__(self):
        """
        Destroys an active board and closes the window.
        """
        cv2.destroyWindow(self.name)

_working = True

position = None
fld = None
cmp_ang = 0

def render(img):
    """
    Rendering everything on the board.
    """
    global position, fld

    ctr_x = 400
    ctr_y = 300

    # Center
    cv2.circle(img, (ctr_x, ctr_y), 80, (255, 200, 200), -1)
    
    # Axes
    cv2.arrowedLine(img, (ctr_x, ctr_y + 50), (ctr_x, ctr_y - 50), (150, 255, 150), 4)
    cv2.arrowedLine(img, (ctr_x - 50, ctr_y), (ctr_x + 50, ctr_y), (255, 150, 150), 4)
    cv2.circle(img, (ctr_x, ctr_y), 6, (150, 150, 255), -1)

    # Trajectory
    cv2.circle(img, (ctr_x, ctr_y), 200, (200, 200, 200), 1)

    # Compass rose
    cv2.putText(img, "N", (ctr_x - 10, ctr_y - 100), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))
    cv2.putText(img, "S", (ctr_x - 10, ctr_y + 120), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))
    cv2.putText(img, "E", (ctr_x + 100, ctr_y + 10), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))
    cv2.putText(img, "W", (ctr_x - 125, ctr_y + 10), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))

    if position is None:
        return

    # Satellite position
    sat_x = int(ctr_x + 200 * np.cos(np.radians(position[0])))    
    sat_y = int(ctr_y - 200 * np.sin(np.radians(position[0])))

    # Expected field vector
    if fld is not None:
        fld_x = int(fld[0] * 100)
        fld_y = -int(fld[1] * 100)
        cv2.arrowedLine(img, (sat_x, sat_y), (sat_x + fld_x, sat_y + fld_y), (0, 0, 255), 3)
        cv2.arrowedLine(img, (ctr_x, ctr_y), (ctr_x + fld_x, ctr_y + fld_y), (0, 0, 255), 3)

    # Compass field vector
    if cmp_ang is not 0:
        cmp_x = int(50 * np.cos(np.radians(cmp_ang)))
        cmp_y = int(-50 * np.sin(np.radians(cmp_ang)))
        cv2.arrowedLine(img, (sat_x, sat_y), (sat_x + cmp_x, sat_y + cmp_y), (0, 255, 0), 3)
        cv2.arrowedLine(img, (ctr_x, ctr_y), (ctr_x + cmp_x, ctr_y + cmp_y), (0, 255, 0), 3)
    
    # Satellite
    cv2.circle(img, (sat_x, sat_y), 5, (50, 50, 0), -1)


# The field and trajectory processors we want to set up
# Field strength was set for the field size to be approx. 0.5 (around 0.57)
# Trajectory radius is based on rough real data, and time is accelerated to
# match a circle in 1.5 mins.
field = TangentialField2D(2.5e19)
trajectory = CircularTrajectory2D(7.371e6, 90)

# The display unit for visualizing everything
# The renderer function is for drawing everything on the board.
display = Display("Indicators window")
display.add_render(render)

# Starting the compass module
compass.init()

t0 = time.time()

while True:

    # Calculating the satellite disposition in space and the expected field we have to 
    # apply according to the models above (circular trajectory and tangential field.)
    dt = time.time() - t0
    position = trajectory.disposition(dt)
    fld = field.field(position)

    cmp_ang = compass.frame()

    display.render()

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

compass.close()