"""
BETA Simulation software for experiment system.
Author: Yotam Salmon
"""

# Importing imaging and calculation modules
print("==========  Importing imaging and calculation modules  ==========")
import numpy as np
import cv2

print("==========  Importing all other modules required  ==========")
# Trajectories and field models
from module.models.trajectory.circular2D import CircularTrajectory2D
from module.models.field.tangential2D import TangentialField2D
from module.models.physics.electricity  import field_coil

# Compass module to process the compass image
import module.compass.compass as compass

# Helmholtz module to control the helmholtz coils
import module.hardware.helmholtz as helmholtz

# DataHub modules
import module.datahub.remote as re
import module.datahub.listener as li

# Trivial imports
import time
import os
import threading
import socket

# Pretty prints! :D
from colorama import init, Fore, Style, Back

class Display(object):
    """
    Display unit for the simulation system.
    """
    def __init__(self, _name, interval=30):
        """
        Creates a new board
        """
        self.screen = np.zeros((600, 800, 3), np.uint8)
        self.display = cv2.namedWindow(_name)
        self.name = _name
        self.renderers = []
        self.interval = interval

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
        return cv2.waitKey(self.interval)

    def __del__(self):
        """
        Destroys an active board and closes the window.
        """
        cv2.destroyWindow(self.name)

"""
The satellite position (height, angle) returned from the trajectory model
"""
position = None

"""
The current field (x, y) returned from the field model
"""
fld = None

"""
The compass angle read by the camera module.
"""
cmp_ang = 0

"""
The magnetometer field read by the magnetometer module (Android gaussmeter)
"""
mgm_field = None

"""
The magnetometer field read by the satellite (Raspberry PI + MPU 9250)
"""
sat_mgm_field = None

def render(img):
    """
    Rendering everything on the board.
    """
    global position, fld

    ctr_x = 400
    ctr_y = 300

    """ Center point """
    cv2.circle(img, (ctr_x, ctr_y), 80, (255, 200, 200), -1)
    
    """ Axes """
    cv2.arrowedLine(img, (ctr_x, ctr_y + 50), (ctr_x, ctr_y - 50), (150, 255, 150), 4)
    cv2.arrowedLine(img, (ctr_x - 50, ctr_y), (ctr_x + 50, ctr_y), (255, 150, 150), 4)
    cv2.circle(img, (ctr_x, ctr_y), 6, (150, 150, 255), -1)

    """ Trajectory """
    cv2.circle(img, (ctr_x, ctr_y), 200, (200, 200, 200), 1)

    """ Compass rose """
    cv2.putText(img, "N", (ctr_x - 10, ctr_y - 100), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))
    cv2.putText(img, "S", (ctr_x - 10, ctr_y + 120), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))
    cv2.putText(img, "E", (ctr_x + 100, ctr_y + 10), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))
    cv2.putText(img, "W", (ctr_x - 125, ctr_y + 10), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))

    if position is None:
        return

    """ Satellite position """
    sat_x = int(ctr_x + 200 * np.cos(np.radians(position[0])))    
    sat_y = int(ctr_y - 200 * np.sin(np.radians(position[0])))

    """ Expected field vector """
    if fld is not None:
        fld_v = np.array(fld) * 50 / (np.linalg.norm(fld) or 1)
        fld_x = int(fld_v[0])
        fld_y = -int(fld_v[1])
        cv2.arrowedLine(img, (sat_x, sat_y), (sat_x + fld_x, sat_y + fld_y), (0, 0, 255), 3)
        cv2.arrowedLine(img, (ctr_x, ctr_y), (ctr_x + fld_x, ctr_y + fld_y), (0, 0, 255), 3)

    """ Magnetometer field vector """
    if mgm_field is not None:
        fld_v = np.array(mgm_field[:2]) * 50 / (np.linalg.norm(mgm_field[:2]) or 1)
        fld_x = int(fld_v[0])
        fld_y = -int(fld_v[1])
        cv2.arrowedLine(img, (sat_x, sat_y), (sat_x + fld_x, sat_y + fld_y), (0, 255, 255), 3)
        cv2.arrowedLine(img, (ctr_x, ctr_y), (ctr_x + fld_x, ctr_y + fld_y), (0, 255, 255), 3)

    """ Satellite Magnetometer field vector """
    if sat_mgm_field is not None:
        fld_v = np.array(sat_mgm_field[:2]) * 50 / (np.linalg.norm(sat_mgm_field[:2]) or 1)
        fld_x = int(fld_v[0])
        fld_y = -int(fld_v[1])
        print(fld_v)
        cv2.arrowedLine(img, (sat_x, sat_y), (sat_x + fld_x, sat_y + fld_y), (255, 255, 0), 3)
        cv2.arrowedLine(img, (ctr_x, ctr_y), (ctr_x + fld_x, ctr_y + fld_y), (255, 255, 0), 3)

    """ Compass field vector """
    if cmp_ang:
        cmp_x = int(50 * np.cos(np.radians(cmp_ang)))
        cmp_y = int(-50 * np.sin(np.radians(cmp_ang)))
        cv2.arrowedLine(img, (sat_x, sat_y), (sat_x + cmp_x, sat_y + cmp_y), (255, 100, 0), 3)
        cv2.arrowedLine(img, (ctr_x, ctr_y), (ctr_x + cmp_x, ctr_y + cmp_y), (255, 100, 0), 3)
    
    """ Satellite """
    cv2.circle(img, (sat_x, sat_y), 5, (50, 50, 0), -1)


"""
The field and trajectory processors we want to set up
Field strength was set for the field size to be approx. 0.5 (around 0.57)
Trajectory radius is based on rough real data, and time is accelerated to
match a circle in 1.5 mins.
"""
field = TangentialField2D(6e19)
trajectory = CircularTrajectory2D(7.371e6, 90)

# Starting the compass module
print("==========  Initializing the compass module  ==========")
try:
    compass.init()
except:
    pass

# Helmholtz connection
print("==========  Connecting to Helmholtz coils  ==========")
helmholtz.init()
time.sleep(0.5)
print("==========  Resetting Helmholtz coils  ==========")
helmholtz.reset()

"""
Updating our IP in the global DataHub
"""
print("==========  Updating our address in the global DataHub  ==========")
hub = re.DataHub("http://rogozin.space/varserver")
hub.set({"lab_ip": socket.gethostbyname(socket.gethostname()), "lab_port": 8090})

"""
Setting up the local DataHub to receive information
"""
print("==========  Initializing the local DataHub  ==========")
li.init()

"""
When everything is ready, we initialize the display.
The display unit for visualizing everything
The renderer function is for drawing everything on the board.
"""
display = Display("Indicators window", 50)
display.add_render(render)

t0 = time.time()
while True:

    # Calculating the satellite disposition in space and the expected field we have to 
    # apply according to the models above (circular trajectory and tangential field.)
    dt = time.time() - t0
    position = trajectory.disposition(dt)
    fld = field.field(position)

    f = np.copy(fld)
    f = f * 1e-4
    f = field_coil(1, 150, f)
    helmholtz.set_current(f)

    try:
        cmp_ang = compass.frame()
        pass
    except:
        cmp_ang = None

    sat_mgm_field = li.get_value("sat_mag")
    if sat_mgm_field is not None:
        sat_mgm_field = sat_mgm_field[0]

    mgm_field = li.get_value("lab_mag")

    os.system("cls")

    print("+-----------------------------------------------+")
    print("| Compass status              |       ", end='')
    print((Style.BRIGHT + Fore.RED + "OFF       ") if not cmp_ang else (Style.BRIGHT + Fore.GREEN + "ON        "), end='')
    print(Style.RESET_ALL + "|")
    print("| Compass angle               |      ", end='')
    print(str(round(((cmp_ang or 0) + 360 % 360), 1)).zfill(5) + "      |")
    
    print("+-----------------------------------------------+")
    print("| Magnetometer status         |       ", end='')
    print((Style.BRIGHT + Fore.RED + "OFF       ") if not mgm_field else (Style.BRIGHT + Fore.GREEN + "ON        "), end='')
    print(Style.RESET_ALL + "|")
    mgm_reading = ",".join(str(round(x)) for x in (mgm_field or [0, 0, 0]))
    lspace = round((17 - len(mgm_reading)) / 2)
    rspace = 17 - len(mgm_reading) - lspace
    print("| Magnetometer                |", end='')
    print(" " * lspace + mgm_reading + " " * rspace + "|")
    
    print("+-----------------------------------------------+")
    print("| Sat magnetometer status     |       ", end='')
    print((Style.BRIGHT + Fore.RED + "OFF       ") if not sat_mgm_field else (Style.BRIGHT + Fore.GREEN + "ON        "), end='')
    print(Style.RESET_ALL + "|")
    mgm_reading = ",".join(str(round(x)) for x in (sat_mgm_field or [0, 0, 0]))
    lspace = round((17 - len(mgm_reading)) / 2)
    rspace = 17 - len(mgm_reading) - lspace
    print("| Sat magnetometer            |", end='')
    print(" " * lspace + mgm_reading + " " * rspace + "|")

    print("+-----------------------------------------------+")
    print("| Helmholtz coils satatus     |       ", end='')
    print((Style.BRIGHT + Fore.RED + "OFF       ") if not helmholtz.connected() else (Style.BRIGHT + Fore.GREEN + "ON        "), end='')
    print(Style.RESET_ALL + "|")
    mgm_reading = ",".join(str(round(x, 3)) for x in (fld if fld is not None else [0, 0]))
    lspace = round((17 - len(mgm_reading)) / 2)
    rspace = 17 - len(mgm_reading) - lspace
    print("| Expected (coils)            |", end='')
    print(" " * lspace + mgm_reading + " " * rspace + "|")
    print("+-----------------------------------------------+")

    if display.render() & 0xFF == ord('q'):
        break

compass.close()
helmholtz.reset()
helmholtz.close()
li.shutdown()
_work = False