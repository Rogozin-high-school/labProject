import os

from module.apps.application import *
import shlex

import example_app

def take_cmd():
    c = input(">>>")
    return list(shlex.shlex(c))

os.system("cls")

inp = take_cmd()
while not "".join(inp) == "exit":
    err = cmd(inp)
    if err is not None:
        print(err)
    inp = take_cmd()