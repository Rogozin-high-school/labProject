"""
Data listener - devices can store data in here
"""

from ..server.httpserver import handler, run

@handler("hello")
def f(req):
    return 200, {}, "World"

thread, httpd = run(("", 8090))