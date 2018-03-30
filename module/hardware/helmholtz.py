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

import serial
import time

class ZUP(object):
    """
    A class that handles the communication with a ZUP60 module.
    It uses serial port for communication.
    """

    def __init__(self, comport : str = None):
        """ Initializes a new ZUP object with a COM port setting. """
        self.comport = comport
        self.ser = None

    def __find_comport(self):
        """ Auto-finds an available COM port that responds to the ZUP ping command. """
        raise NotImplementedError\
            ("The __find_comport method of the class ZUP was not yet implemented.")

    def connect(self) -> bool:
        """ Connects to a ZUP device. """
        if self.comport == None:
            raise NotImplementedError("Automatically finding COM ports is not implemented")
        
        if self.ser:
            raise Exception("ZUP object is already connected to port")

        self.ser = serial.Serial(self.comport, 9600, 8, serial.PARITY_NONE, 1, 500, True, False, False, 500)
        self.ser.close()
        self.ser.open()

        time.sleep(0.015)
        
        if not self.ser.isOpen():
            raise Exception("Error opening connection to ZUP device on port " + self.comport)

        return True

    def disconnect(self) -> None:
        """ Disconnects from the ZUP device """
        if not self.ser or not self.ser.isOpen():
            raise Exception("Not currently connected to ZUP device")

        self.ser.close()
        self.ser = None


    def send(self, cmdtxt : str) -> str:
        self.ser.write(bytes(cmdtxt, "ascii"))
        time.sleep(0.015)
        
        if self.ser.in_waiting:
            return self.ser.readline()
    
    def addr(self, a : int):
        """
        Sends an :ADDRn; command. 
        a - number 1-31, symbols which ZUP device should comply with the next commands.
        """

        if not 0 < a < 32:
            raise ValueError("Address must be between 1 and 31")

        self.send(":ADDR{0:0>2};".format(a))
        return True

    def set_volt(self, volt : float):
        """
        Sets the Epsilon voltage of the device.
        volt - the voltage, in volts.
        """

        if not 0 <= volt <= 60:
            raise ValueError("Voltage must be between 0 and 60")

        self.send(":VOL{:05.2f};".format(volt))
        return True