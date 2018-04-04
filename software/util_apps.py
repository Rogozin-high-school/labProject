import module.apps.application as application

class start(application.ApplicationBase):
    """
    Starts different apps
    """ 

    def __startup__(self):
        pass

    def __app__(self, cmd):
        success, status = application.start(cmd[2])
        if not success:
            print("Error: " + status)

    def __commands__(self):
        return {
            "app": self.__app__,
            "": self.__app__
        }

    def __details__(self):
        return {
            "full_name": "Starter app",
            "description": "Starts other apps",
            "version": "1.0",
            "developer": "Yotam Salmon",
            "version_date": "04 Apr 2018"
        }

    def __help__(self):
        return "No help available for this app"

    def __clean__(self):
        pass

application.load(start())
application.start("start")

import os

class cls(application.ApplicationBase):
    """
    Cleans the screen
    """ 

    def __startup__(self):
        pass

    def __cls__(self, cmd):
        os.system("cls")

    def __commands__(self):
        return {
            "": self.__cls__
        }

    def __details__(self):
        return {
            "full_name": "Clear screen app",
            "description": "Clears the screen",
            "version": "1.0",
            "developer": "Yotam Salmon",
            "version_date": "04 Apr 2018"
        }

    def __help__(self):
        return "No help available for this app"

    def __clean__(self):
        pass

application.load(cls())
application.start("cls")
