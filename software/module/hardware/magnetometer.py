"""
Retrieves data from the laboratory magnetometer device.
Infrastructure: 
    Computer <-> Arduino <-> Magnetometer
"""

import serial
import serial.tools.list_ports as lp

import time

class Magnetometer(object):
    """ A class that handles the reading of a magnetometer sensor """

    def __init__(self, comport=None):
        """ Sets a new connection to a magnetometer """
        self.comport = comport or self.__find_comport()

    def __find_comport(self):
        """ Auto-finds an available COM port that responds to the magnetometer ping command. """
        
        avail = [x.device for x in lp.comports() if "Arduino Uno" in x.description]
        return avail[0] if avail else None

    def connect(self):
        """ Connects to the magnetometer port """
        self.ser = serial.Serial(self.comport, 9600)
        self.ser.close()
        self.ser.open()

    def get_field(self):
        """ Returns the magnetometer reading as a numpy array of length 3 """
        self.ser.write(b"F")
        time.sleep(0.01)
        if self.ser.in_waiting == 0:
            return None
        return [float(i.strip()) for i in str(self.ser.readline(), "ascii").split(",")]

    def calibrate(self):
        self.ser.write(b"C")
        time.sleep(11)
        self.ser.read_all()

    def get_horizontal_direction(self):
        """ Returns the angle across the [xy] plane of the magnetic field vector """
        m = self.get_field()
        return m[3] if m else 0

    def disconnect(self):
        """ Closes the connection with the magnetometer device. """
        self.ser.close()
        self.ser = None