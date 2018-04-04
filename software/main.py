from module.apps.application import *
import shlex

import example_app

start("example_app")

def take_cmd():
    cmd = input(">>>")
    return list(shlex.shlex(cmd))

inp = take_cmd()
while not "".join(inp) == "exit":
    err = cmd(inp)
    if err is not None:
        print(err)
    inp = take_cmd()