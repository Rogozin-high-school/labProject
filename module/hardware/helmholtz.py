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
import enum

class RemoteMode(enum.Enum):
    """
    To represent different remote modes
    """
    REMOTE = 1
    LATCHED = 2

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
        time.sleep(0.018)
        
        if self.ser.in_waiting:
            return str(self.ser.readline(), "ascii")[:-2]
    
    def addr(self, a : int) -> bool:
        """
        Sends an :ADDRn; command. 
        a - number 1-31, symbols which ZUP device should comply with the next commands.
        """

        if not 0 < a < 32:
            raise ValueError("Address must be between 1 and 31")

        self.send(":ADR{0:0>2};".format(a))
        return True

    def set_volt(self, volt : float) -> bool:
        """
        Sets the output voltage value in volts. Thie programmed voltage is the actual output
        at constant-voltage mode or the voltage limit at constant-current mode.

        volt - the voltage, in volts.
        """

        if not 0 <= volt <= 60:
            raise ValueError("Voltage must be between 0 and 60")

        self.send(":VOL{:05.2f};".format(volt))
        return True

    def clear(self) -> bool:
        """
        Clears the communication buffer and the following registers:
            1. Operational status register
            2. Alarm (fault status register)
            3. Programming error register
        """
        self.send(":DCL;")
        return True

    def set_remote(self, rmt : int) -> None:
        """
        Sets the power supply to local or remote mode.
        rmt - 0: Transition from remote to local mode
            - 1: Transition from latched remote to non-latched remote
            - 2: Latched remote: transition back to local mode or to non-latched remote.
        """
        if not 0 <= rmt < 3:
            raise Exception("Remote mode shouldbe between 0 and 2")

        self.send(":RMT{:d};".format(rmt))
        return True

    def get_remote(self) -> RemoteMode:
        """
        Returns the remote/local setting.
        """

        rmt = int(self.send(":RMT?;")[2])
        return RemoteMode(rmt)

    def get_model(self) -> str:
        """
        Returns the power supply model identification as an ASCII string.
        """

        return self.send(":MDL?;")

    def get_software(self) -> str:
        """
        Returns the software version as an ASCII string
        """

        return self.send(":REV?;")

    def get_p_volt(self) -> float:
        """
        Returns the present programmed output voltage value.
        """

        return float(self.send(":VOL!;")[2:])

    def get_volt(self) -> float:
        """
        Returns the actual output voltage. The actual voltage range is the same as the programming range.
        """

        return float(self.send(":VOL?;")[2:])

    def set_amp(self, amp : float) -> None:
        """
        Sets the output current in Amperes. This programmed currnet is the actual output voltage at
        constant-current mode or the current limit in constnat-voltage mode. 
        """

        if not amp <= 0 <= 3.5:
            raise ValueError("Current can only be between 0A and 3.5A")

        self.send(":CUR{:05.3f};".format(amp))
        return True

    def get_p_amp(self) -> float:
        """
        Returns the present programmed output current.
        """

        return float(self.send(":CUR!;")[2:])

    def get_amp(self) -> float:
        """
        Returns the actual output current.
        """

        return float(self.send(":CUR?;")[2:])
