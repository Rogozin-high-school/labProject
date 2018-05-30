"""
Controls an array of coils.
"""

from .supplies import *
from .BOX import *


import time

class CoilArray(object):

    def __init__(self, log = print):
        log("Connecting to ZUP supplies")
        self.sups = None
        self.box = None
        
        self.sups = self.get_supplies()
        if self.sups[0] == None or self.sups[1] == None:
            log("Failed to locate ZUP supplies")
            self.close()
            self.sups = None
            return

        log("Connecting to BOX")
        try:
            self.box = BOX()
            self.box.connect()
        except:
            log("Failed to connect to BOX device")
            self.box = None
            return

        log("Determining coil resistances")
        self.vals = [0, 0, 0]
        self.res = self.get_resistances()
        print("Coil resistances: " + str(self.res))
        log("Done initializing coil array")

    def get_supplies(self):
        sups = ZUP.get_comports()
        x = [i for i in sups if i[1] == 1]
        y = [i for i in sups if i[1] == 2]
        z = [i for i in sups if i[1] == 3]

        
        _x = x[0][0] if x else None
        _y = y[0][0] if y else None
        _z = z[0][0] if z else None

        return [_x, _y, _z]

    def is_connected(self) -> bool:
        """ Checks if the coil array has an ongoing connection with ZUP"""
        if self.sups == None or self.box == None :
            return False
        return True

    def set_cur(self, index, cur):
        if self.sups == None or self.box == None:
            return False

        if cur * self.vals[index] <= 0:
            self.set_supply_sign(index, cur)
        self.vals[index] = cur
        try:
            self.sups[index].set_amp(abs(cur))
            self.sups[index].set_volt(min(abs(cur * self.res[index]), 58))
        except:
            return False
        return True

    def get_resistances(self):
        res = []
        for x in self.sups:
            if x == None:
                res.append(0)
                continue

            x.set_volt(1)
            x.set_amp(1)
            time.sleep(0.25)
            
            x.set_out(1)

            v = x.get_volt()
            a = x.get_amp()
            while v <= 0 or v >= 100 or a == 0 or (v / a) < 3 or (v / a) > 15:
                time.sleep(0.1)
                v = x.get_volt()
                a = x.get_amp()
            
            if a == 0:
                res.append(0)
            else:
                res.append(v / a)
            
            x.set_volt(0)

        return res

    def reset_supplies(self):
        if self.sups == None or self.box == None:
            return False

        for x in self.sups:
            if x:
                x.set_out(OutputMode.ON)
                x.set_amp(0)
                x.set_volt(0)

        self.box.straight(0)
        self.box.straight(1)
        self.box.straight(2)
        return True

    def close(self):
        if self.sups != None:
            for x in self.sups:
                if x:
                    x.disconnect()
        if self.box:
            self.box.disconnect()

    def zero_supply(self, index):
        if self.sups[index]:
            self.sups[index].set_volt(0)
            i = 0
            while self.sups[index].get_volt() > 0.1 and i < 3:
                print("Waiting for supply to shut down. Voltage: " + str(self.sups[index].get_volt()))
                time.sleep(0.1)
                self.sups[index].set_volt(0)
                time.sleep(0.2)
                i += 1
    
    def set_supply_sign(self, index, sign):
        if self.sups[index]:
            volt = self.sups[index].get_volt()
            self.zero_supply(index)
            if sign >= 0:
                self.box.straight(index)
            else:
                self.box.flip(index)
            self.sups[index].set_volt(min(58, volt))