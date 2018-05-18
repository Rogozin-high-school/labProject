"""
Helmholtz module for controlling the current around the axes
"""

from .coilarray import *

arr = None

def init():
    global arr

    while arr is None:
        arr = CoilArray()

def reset():
    arr.reset_supplies()

def set_current(current):
    print(current)
    for i, e in enumerate(current):
        arr.set_cur(i, e)

def close():
    arr.close()