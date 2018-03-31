"""
For serving our website and REST services of the Rogozin Space Lab.
Author: Yotam Salmon
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
from socketserver import ThreadingMixIn

_get_handlers = {}
_post_handlers = {}

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global _get_handlers

        handler = self.path[1:].split("#")[0].split("?")[0]
        
        if handler in _get_handlers.keys():
            response, headers, content = _get_handlers[handler](self)
            
            self.send_response(response)
            for h, v in headers:
                self.send_header(h, v)

            self.end_headers()

            self.wfile.write(bytes(content, "utf-8") if type(content) == str else content)

    def do_POST(self):
        global _post_handlers

        handler = self.path[1:].split("#")[0].split("?")[0]
        
        if handler in _post_handlers.keys():
            response, headers, content = _post_handlers[handler](self)
            
            self.send_response(response)
            for h, v in headers:
                self.send_header(h, v)

            self.end_headers()

            self.wfile.write(bytes(content, "utf-8") if type(content) == str else content)


def handler(url, method = "GET"):
    global _get_handlers, _post_handlers
    def handler_decorator(func):
        global handlers
        (_get_handlers if method.upper() == "GET" else _post_handlers)[url] = func
        return func
    return handler_decorator

def run(addr):
    httpd = ThreadedHTTPServer(addr, RequestHandler)
    thread = threading.Thread(target=httpd.serve_forever)
    thread.start()
    return thread, httpd