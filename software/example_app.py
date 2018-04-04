from module.apps.application import ApplicationBase, load

import util_apps

class example_app(ApplicationBase):
    def __startup__(self):
        print("ExampleApp has been started up! I'm so cool jezuz")
        self.i = 42

    def __be_cool__(self, cmd):
        print("This command is kinda awesome" + str(self.i))

    def __commands__(self):
        return {
            "becool": self.__be_cool__
        }

    def __details__(self):
        return {
            "full_name": "Example App",
            "description": "This is an example class that represents an application.",
            "version": "0.1",
            "developer": "Lab Team 2017-18",
            "version_date": "01 Apr 18"
        }

    def __help__(self, cmd : str):
        return ({
            "": "This is a module. You can call the command 'becool'",
            "becool": "Just prints awesome stuff to the command line"
        })[cmd]

    def __clean__(self):
        print("'I'm outta here'\r\n    - ExampleApp, 2018")

load(example_app())