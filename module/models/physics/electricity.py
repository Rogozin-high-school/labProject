"""
The electricity module should help us with the mathematics required for converting physical
quantities (as magnetic field vectors) to the required electrical quantities (voltage, current).
"""

import numpy as np

# Mathematical & Physical constants that can help us later
π = 3.1415926535
μ0 = 4e-7 * π
c = μ0 * (4 / 5) ** (3 / 2)

def coil_field(R, i, N):
    """ To calculate the field of a pair of Helmholtz coils and return the magnitude of the field """
    return c * N * i / R

def field_coil(R, N, B):
    """ To calculate the current required for creating a magnetic field. Return value in Amperes """
    return B * R / (N * c)

def ohm_current(v, r):
    """ Calculates the circuit required current for a certain voltage and resistance, according to Ohm's law """
    return v / r

def ohm_voltage(i, r):
    """ Calculates the circuit voltage by current and resistance, according to Ohm's law """
    return i * r