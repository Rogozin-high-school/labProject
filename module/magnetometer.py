"""
Retrieves data from the laboratory magnetometer device.
Infrastructure: 
    Computer <-> Arduino <-> Magnetometer
"""

class Magnetometer(object):
    """ A class that handles the reading of a magnetometer sensor """

    def __init__(self, comport=None):
        """ Sets a new connection to a magnetometer """
        self.comport = comport

    def __find_comport(self):
        """ Auto-finds an available COM port that responds to the magnetometer ping command. """
        raise NotImplementedError\
            ("The __find_comport method of the class Magnetometer was not yet implemented.")

    def connect(self):
        """ Connects to the magnetometer port """
        raise NotImplementedError\
            ("The connect method of the class Magnetometer was not yet implemented.")

    def get_field(self):
        """ Returns the magnetometer reading as a numpy array of length 3 """
        raise NotImplementedError\
            ("The get_field method of the class Magnetometer was not yet implemented.")

    def get_horizontal_direction(self):
        """ Returns the angle across the [xy] plane of the magnetic field vector """
        raise NotImplementedError\
            ("The get_horizontal_direction method of the class Magnetometer was not yet implemented")