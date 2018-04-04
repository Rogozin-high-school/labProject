import module.apps.application as application

class start(application.ApplicationBase):
    """
    Starts different apps
    """ 

    def __startup__(self):
        pass

    def __app__(self, cmd):
        application.start(cmd[2])

    def __commands__(self):
        return {
            "app": self.__app__
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