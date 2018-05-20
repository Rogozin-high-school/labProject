"""
Data listener - devices can store data in here
"""

from ..server.httpserver import handler, run
from ..server.httphelper import json_post

import json
import time

_data = {}
_timestamp = {}

@handler("set", "POST")
def set(req):
    global _data

    j = json_post(req)

    if type(j) != list:
        return 400, {"Access-Control-Allow-Origin": "*"}, "Must be an array"

    resps = []

    for i in j:
        if "id" not in i.keys():
            resps.append({"success": False, "error": "ID not in request body"})
            continue

        if "value" not in i.keys():
            resps.append({"success": False, "error": "value not in request body"})
            continue

        _data[i["id"]] = i["value"]
        _timestamp[i["id"]] = time.time()
        resps.append({"success": True})
    
    return 200, {"Access-Control-Allow-Origin": "*"}, json.dumps(resps)

@handler("get", "POST")
def get(req):
    global _data

    j = json_post(req)

    if type(j) != list:
        return 400, {"Access-Control-Allow-Origin": "*"}, "List only please"

    resps = []
    for i in j:
        if "id" not in i.keys():
            resps.append({"success": False, "error": "ID not in request body"})
            continue

        if i["id"] not in _data.keys():
            resps.append({"success": False, "error": "Var not found"})
            continue

        resps.append({"success": True, "content": _data[i["id"]]})

    return 200, {"Access-Control-Allow-Origin": "*"}, json.dumps(resps)

def get_value(var):
    global _data

    return _data[var] if var in _data.keys() else None

def get_timestamp(var):
    global _timestamp
    
    return _timestamp[var] if var in _timestamp.keys() else 0

def set_value(var, val):
    global _data

    _data[var] = val

thread, httpd = None, None

def init():
    global thread, httpd
    thread, httpd = run(("", 8090))

def shutdown():
    global httpd
    httpd.shutdown()