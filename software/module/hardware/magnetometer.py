"""
Retrieves data from the laboratory magnetometer device.
Infrastructure: 
    Computer <-> Arduino <-> Magnetometer
"""

import urllib.request
import json
import time

def get_field():
    body = bytes(
        json.dumps([
            {"id": "magnetometer", "password": "ronherepov"},
            {"id": "sat_mag"}
            ]
        ), "utf-8")
    req = urllib.request.urlopen(
        "http://rogozin.space/varserver/get.php",
        body
        )
    res = json.loads(str(req.read(), "utf-8"))
    if res[0]["success"] == True and res[1]["success"] == True:
        return res[0]["content"], res[1]["content"]
    return None, None