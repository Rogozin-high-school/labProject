"""
The electricity module should help us with the mathematics required for converting physical
quantities (as magnetic field vectors) to the required electrical quantities (voltage, current).
"""

import numpy as np

# Mathematical & Physical constants that can help us later
π = 3.1415926535
μ0 = 4e-7 * π

def coil_field(coil_radius, current, N):
    """ To calculate the field of a Helmholtz coil and return the magnitude of the field"""
    return μ0 * N * current / (2 * coil_radius)

def field_coil(coil_radius, N, field):
    """ To calculate the current required for creating a magnetic field. Return value in Amperes """
    return 2 * field * coil_radius / (μ0 * N)

