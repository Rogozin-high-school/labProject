import serial
import time
import enum
import serial.tools.list_ports

class BOX(object): #FUCK YOUR CONVENSIONS
    """
    A class that handles the communication with the BOX Yotam built (and Koren Helped with).
    It uses serial port for communication.
    """

    def __init__(self, comport : str = None):
        """ Initializes a new BOX object with a COM port setting. """
        self.ser = None
        if comport == None:
            self.__find_comport()
        else:
            self.comport = comport

    def __find_comport(self):
        """ Auto-finds an available COM port that responds to the BOX ping command. """
        comlist = serial.tools.list_ports.comports()
        for com in comlist:
            if com.description.find("Arduino Uno") != -1:
                self.comport = com.device
                return
        raise Exception("ZUP comport could not found")
				
    def ping(com):
        z = ZUP(com)
        z.connect()
        for i in range(1,4):
            z.addr(i)
            if(z.get_model() != None):
                return z, i
        return z, None
		
		

    def connect(self) -> bool:
        """ Connects to a ZUP device. """
        if self.comport == None:
            raise NotImplementedError("Automatically finding COM ports is not implemented")
        
        if self.ser:
            raise Exception("ZUP object is already connected to port")

        self.ser = serial.Serial(self.comport, 9600)
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
    
    def addr(self, a : int) -> "ZUP":
        """
        Sends an :ADDRn; command. 
        a - number 1-31, symbols which ZUP device should comply with the next commands.
        """

        if not 0 < a < 32:
            raise ValueError("Address must be between 1 and 31")

        self.send(":ADR{0:0>2};".format(a))
        return self

    def clear(self) -> "ZUP":
        """
        Clears the communication buffer and the following registers:
            1. Operational status register
            2. Alarm (fault status register)
            3. Programming error register
        """
        self.send(":DCL;")
        return self
    
    def flip(self, a : int) -> str:
        """
        sends the flip function to the BOX
        a - a number between 0 to 2 that decides the strenght of the current
        """
        if a > 2 or a < 0:
            raise ValueError("flip value must be between 0 and 2")
        return self.send("FLP" + str(a) + ";")

    def straight(self, a : int) -> str:
        """
        sends the straight function to the BOX
        a - a number between 0 to 2 that decides the strenght of the current
        """
        if a > 2 or a < 0:
            raise ValueError("straight value must be between 0 and 2")
        return self.send("STR" + str(a) + ";")

    def info(self) -> str:
        """
        sends the info function to the BOX
        """ 
        a = self.send("INF;")
        return a

