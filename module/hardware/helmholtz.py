"""
This module communicates with the Helmholtz coils via a serial interface.
It creates a Python interface for sending and receiving commands in their purest
form, as described in the TDK-Lambda ZUP60-3.5 manual.

Remarks:
1.  One ZUP class can control multiple Helmholtz coils (multiple power supplies)
2.  The helmholtz coils will be addressed with a unique ID (or something similar).
    The protocol of communication will be set on the Arduino. Basic structure will
    be:
                             <-> Power Supply
        Computer <-> Arduino <-> Power Supply
                             <-> Power Supply
"""

class ZUP(object):
    """
    A class that handles the communication with a ZUP60 module.
    It uses serial port for communication.
    """

    def __init__(self, comport=None):
        """ Initializes a new ZUP object with a COM port setting. """
        self.comport = comport

    def __find_comport(self):
        """ Auto-finds an available COM port that responds to the ZUP ping command. """
        raise NotImplementedError\
            ("The __find_comport method of the class ZUP was not yet implemented.")

    def connect(self):
        """ Connects to a ZUP device. """
        raise NotImplementedError\
            ("The connect method of the class ZUP was not yet implemented.")

			
"""
This is a test script I have created to communicate with the power supply.
We can use it to create the communication port. 
After the class creation is done, we may want to remove this code.
"""

import serial
import threading
import time

s = serial.Serial("COM13", 9600, 8, serial.PARITY_NONE, 1, 500, True, False, False, 500)
s.close()
s.open()

i = input()
while i != "exit":
    s.write(bytes(i, "ascii"))
    time.sleep(0.015)
    if (s.in_waiting):
        print(s.readline())
    i = input()
s.close()