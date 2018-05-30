"""
BETA Simulation software for experiment system.
Author: Yotam Salmon
"""

# Importing imaging and calculation modules
print("==========  Importing imaging and calculation modules".ljust(70) + "==========")
import numpy as np
import cv2

print("==========  Importing all other modules required".ljust(70) + "==========")
# Trajectories and field models
from module.models.trajectory.circular2D import CircularTrajectory2D
from module.models.field.tangential2D import TangentialField2D
from module.models.field.constant import ConstantField
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
cmp_frame = None
cmp_show = False

"""
The magnetometer field read by the magnetometer module (Android gaussmeter)
"""
mgm_field = None
mgm_show = False

"""
The magnetometer field read by the satellite (Raspberry PI + MPU 9250)
"""
sat_mgm_field = None
sat_mgm_show = False

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
    if mgm_field is not None and mgm_show:
        fld_v = np.array(mgm_field[:2]) * 50 / (np.linalg.norm(mgm_field[:2]) or 1)
        fld_x = int(fld_v[0])
        fld_y = -int(fld_v[1])
        cv2.arrowedLine(img, (sat_x, sat_y), (sat_x + fld_x, sat_y + fld_y), (0, 255, 255), 3)
        cv2.arrowedLine(img, (ctr_x, ctr_y), (ctr_x + fld_x, ctr_y + fld_y), (0, 255, 255), 3)

    """ Satellite Magnetometer field vector """
    if sat_mgm_field is not None and sat_mgm_show:
        fld_v = np.array(sat_mgm_field[:2]) * 50 / (np.linalg.norm(sat_mgm_field[:2]) or 1)
        fld_x = int(fld_v[0])
        fld_y = -int(fld_v[1])
        cv2.arrowedLine(img, (sat_x, sat_y), (sat_x + fld_x, sat_y + fld_y), (255, 255, 0), 3)
        cv2.arrowedLine(img, (ctr_x, ctr_y), (ctr_x + fld_x, ctr_y + fld_y), (255, 255, 0), 3)

    """ Compass field vector """
    if cmp_ang and cmp_show:
        cmp_x = int(50 * np.cos(np.radians(cmp_ang)))
        cmp_y = int(-50 * np.sin(np.radians(cmp_ang)))
        cv2.arrowedLine(img, (sat_x, sat_y), (sat_x + cmp_x, sat_y + cmp_y), (255, 100, 0), 3)
        cv2.arrowedLine(img, (ctr_x, ctr_y), (ctr_x + cmp_x, ctr_y + cmp_y), (255, 100, 0), 3)
    
    """ Satellite """
    cv2.circle(img, (sat_x, sat_y), 5, (50, 50, 0), -1)

    """ Compass frame"""
    # if cmp_frame is not None:
    #     img[0:150,0:200] = cmp_frame

    """ Field caption """
    cv2.putText(img, "Field: " + field_name, (ctr_x - 110, 30), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))

    """ Legends """
    cv2.putText(img, "Gaussmeter " + ("ON" if mgm_show else "OFF"),     (600, 450), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255 if mgm_show else 0)       )
    cv2.putText(img, "Sat Magnet " + ("ON" if sat_mgm_show else "OFF"), (600, 475), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255 if sat_mgm_show else 0)   )
    cv2.putText(img, "Compass "    + ("ON" if cmp_show else "OFF"),     (600, 500), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255 if cmp_show else 0)       )


def calc_orientation(field, sat_field):
    tf =  np.degrees(np.arctan2(field[1], field[0]))
    sf = np.degrees(np.arctan2(sat_field[1], sat_field[0]))
    

    return 90 + tf - sf

"""
The field and trajectory processors we want to set up
Field strength was set for the field size to be approx. 0.5 (around 0.57)
Trajectory radius is based on rough real data, and time is accelerated to
match a circle in 1.5 mins.
"""

fields = [
    ConstantField([0, 0, 0]),
    ConstantField([-3, -1, 0]),
    TangentialField2D(10e19)
]
field_names = [
    "Natural Earth Field",
    "Constant Field",
    "Tangential Field"
]

field = fields[0]
field_name = field_names[0]
trajectory = CircularTrajectory2D(7.371e6, 300)

# Starting the compass module
print("==========  Initializing the compass module".ljust(70) + "==========")
try:
    compass.init()
except:
    pass

# Helmholtz connection
print("==========  Connecting to Helmholtz coils".ljust(70) + "==========")
helmholtz.init()
time.sleep(0.5)
print("==========  Resetting Helmholtz coils".ljust(70) + "==========")
helmholtz.reset()
print(helmholtz.arr.sups)

"""
Updating our IP in the global DataHub
"""
print("==========  Updating our address in the global DataHub".ljust(70) + "==========")
hub = re.DataHub("http://rogozin.space/varserver")
hub.set({"lab_ip": socket.gethostbyname(socket.gethostname()), "lab_port": 8090})

"""
Setting up the local DataHub to receive information
"""
print("==========  Initializing the local DataHub".ljust(70) + "==========")
li.init()

print(">>>> PRESS ENTER TO START THE SIMULATION <<<<")
input()

"""
When everything is ready, we initialize the display.
The display unit for visualizing everything
The renderer function is for drawing everything on the board.
"""
display = Display("Indicators window", 75)
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
        cmp_ang, cmp_frame = compass.frame()
        cmp_frame = cv2.resize(cmp_frame, (200, 150))
        pass
    except:
        cmp_ang = None

    sat_mgm_field, sat_ping = li.get_value("sat_mag"), time.time() - (li.get_timestamp("sat_mag") or 0)
    if sat_ping < 3 and sat_mgm_field is not None:
        sat_mgm_field = sat_mgm_field[0]
    else:
        sat_mgm_field = None

    mgm_field, mgm_ping = li.get_value("lab_mag"), time.time() - li.get_timestamp("lab_mag")
    if mgm_ping > 3:
        mgm_field = None

    dtheta = None
    if sat_mgm_field is not None:
        dtheta = calc_orientation(fld, sat_mgm_field)
        li.set_value("sat_rot", [0, 0, -dtheta])

    os.system("cls")
    print(Style.BRIGHT + Fore.MAGENTA, end='')
    print("          Experiment system software" + Style.RESET_ALL)
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
    print("")
    print("Press " + Fore.LIGHTGREEN_EX + "t" + Style.RESET_ALL + " to set magnetorquer to 1")
    print("Press " + Fore.LIGHTCYAN_EX + "y" + Style.RESET_ALL + " to set magnetorquer to 0")
    print("Press " + Fore.LIGHTRED_EX + "u" + Style.RESET_ALL + " to set magnetorquer to -1")

    print (dtheta)

    key = display.render()
    if key & 0xFF == ord('q'):
        break

    print(str(key) + ": " + (chr(key) if key != -1 else ""))

    if key & 0xFF == ord('t'):
        li.set_value("sat_magnetorquer", 1)
    elif key & 0xFF == ord('y'):
        li.set_value("sat_magnetorquer", 0)
    elif key & 0xFF == ord('u'):
        li.set_value("sat_magnetorquer", -1)

    elif key & 0xFF == ord('1'):
        field = fields[0]
        field_name = field_names[0]
    elif key & 0xFF == ord('2'):
        field = fields[1]
        field_name = field_names[1]
    elif key & 0xFF == ord('3'):
        field = fields[2]
        field_name = field_names[2]

    elif key & 0xFF == ord('a'):
        mgm_show = True
    elif key & 0xFF == ord('z'):
        mgm_show = False

    elif key & 0xFF == ord('s'):
        sat_mgm_show = True
    elif key & 0xFF == ord('x'):
        sat_mgm_show = False
    
    elif key & 0xFF == ord('d'):
        cmp_show = True
    elif key & 0xFF == ord('c'):
        cmp_show = False

    elif key & 0xFF == ord('r'):
        t0 = time.time()

compass.close()
helmholtz.reset()
helmholtz.close()
li.shutdown()
_work = False