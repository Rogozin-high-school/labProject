"""
Module for dynamic loading of applications into the laboratory computer main software.
Author: Yotam Salmon
"""

from abc import ABC, abstractmethod
import traceback

class ApplicationBase(ABC):
    """
    Represents an application.
    The subclass names should be all lower case letters, and they will be used to call
    the applications from the command line.
    """

    @abstractmethod
    def __startup__(self):
        """
        Calls once the application should be loaded.
        This is responsible for everything that starts the application up.
        """
        pass

    @abstractmethod
    def __commands__(self):
        """
        Should return a list of available commands in the form of a dictionary.
        Keys - the command strings.
        Values - the function to call when a command is called.
        For example:
            {
                "init": self._init_,
                "pause": self._pause_
            }

        To call a command via the cmd:
            >>> <application_name> <command_name> [arguments]:

        The function will receive a list parameter with the command (including the app name and the command name):
        For example, entering the command:
            >>> compass calibrate -c 8
        Will give a list parameter:
            ["compass", "calibrate", "-c", "8"]
        """
        pass

    @abstractmethod
    def __details__(self):
        """
        Should return the application details in a form of a dictionary.
        For example:
            {
                "full_name": "Base Application",
                "description": "This is the base class for all applications"
                "version": "1.0.4",
                "developer": "Yotam Salmon",
                "version_date": "31 Mar 2018" // The date when you last changed the version parameter 
            }
        """
        pass

    @abstractmethod
    def __help__(self, command):
        """
        Should return a help-string for the specified command. 
        If the command parameter is None, means you have to return a general help-string for the application.
        """

    @abstractmethod
    def __clean__(self):
        """
        To deallocate, clear APIs and memory and clean everything when the application is finished.
        """
        pass

"""
To store all the loaded apps. Keys - strings, Values - ApplicationBase subclasses.
"""
_apps = {}

def load(app : ApplicationBase):
    """
    Loads an application.
    """
    global _apps

    app.loaded = False
    _apps[type(app).__name__] = app

def start(app : str):
    """
    Starts an already-loaded application.
    """
    global _apps

    if app not in _apps.keys():
        return False, "App not found"
    
    if hasattr(_apps[app], "loaded") and _apps[app].loaded:
        return False, "App already loaded"
    
    _apps[app].__startup__()
    _apps[app].loaded = True
    return True, None
    

def close(app : str):
    """
    Closes a started application.
    """
    global _apps

    if app not in _apps.keys():
        return False, "App not found"
    
    if hasattr(_apps[app], "loaded") and not _apps[app].loaded:
        return False, "App is not loaded"
    
    _apps[app].__clean__()
    _apps[app].loaded = False
    return True, None

def get_help(app : str, cmd : str):
    """
    Returns a help-string for a specific application and command.
    """
    global _apps

    if app not in _apps.keys():
        return False, "App not found"

    return _apps[app].__help__(cmd)

def cmd(cmd):
    if len(cmd) < 1:
        return "No application specified"

    if cmd[0] not in _apps.keys():
        return "App not found"

    if not _apps[cmd[0]].loaded:
        return "App not loaded"

    if len(cmd) < 2:
        return "No command specified"

    if cmd[1] not in _apps[cmd[0]].__commands__():
        return "Unregistered command"

    try:
        _apps[cmd[0]].__commands__()[cmd[1]](cmd)
    except Exception as ex:
        print(traceback.format_exc())
        print(ex)
    return None