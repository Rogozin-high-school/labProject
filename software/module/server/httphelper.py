"""
Helper functions for HTTP communication
"""

import sys
import json
import base64
from http.cookies import SimpleCookie
import urllib.parse

from .httpserver import RequestHandler

def post(req: RequestHandler):
    """
    Extract the POST body from a request.
    """
    if not "Content-Length" in req.headers.keys():
        return None
    try:
        content_length = int(req.headers["Content-Length"])
    except:
        return None
    return req.rfile.read(content_length)

def json_post(req: RequestHandler):
    """
    Extracts and parses a json POST data.
    """
    content = post(req)
    if content is None:
        return None
    try:
        return json.loads(content.decode("utf-8"))
    except:
        return None

def querystring(req : RequestHandler) -> dict:
    """
    Gets and parses the query string from a request to a dictionary (key: val)
    """
    try:
        p = urllib.parse.urlparse(req.path)
        qs = urllib.parse.parse_qs(p.query)
        return qs
    except:
        return None