"""
Helmholtz module for controlling the current around the axes
"""

from .supplies import *

COIL_RESISTANCE = 36.9 # Measured value. Can be changed

X = None
Y = None
Z = None

def init():
    global X, Y, Z

    sups = ZUP.get_comports()
    x = [i for i in sups if i[1] == 1]
    y = [i for i in sups if i[1] == 2]
    z = [i for i in sups if i[1] == 3]

    X = x[0][0] if x else None
    Y = y[0][0] if y else None
    Z = z[0][0] if z else None

    print(X)
    print(Y)
    print(Z)

def reset():
    global X, Y, Z

    if X:
        X.set_out(OutputMode.ON)
        X.set_amp(0)
        X.set_volt(0)
    
    if Y:
        Y.set_out(OutputMode.ON)
        Y.set_amp(0)
        Y.set_volt(0)

    if Z:
        Z.set_out(OutputMode.ON)
        Z.set_amp(0)
        Z.set_volt(0)

def close():
    global X, Y, Z

    if X:
        X.disconnect()

    if Y:
        Y.disconnect()

    if Z:
        Z.disconnect()

def set_current(axes):
    global X, Y, Z, COIL_RESISTANCE

    if X:
        X.set_amp(axes[0] * 1.01)
        X.set_volt(axes[0] * 1.01 * COIL_RESISTANCE)

    if Y:
        Y.set_amp(axes[1] * 1.01)
        Y.set_volt(axes[1] * 1.01 * COIL_RESISTANCE)

    if Z:
        Z.set_amp(axes[2] * 1.01)
        Z.set_volt(axes[2] * 1.01 * COIL_RESISTANCE)