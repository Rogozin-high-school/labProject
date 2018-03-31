"""
For serving our website and REST services of the Rogozin Space Lab.
Author: Yotam Salmon
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import threading
import os
import re

_get_handlers = {}
_post_handlers = {}
_settings = {}

def mime_content_type(filename):
    """Get mime type
    :param filename: str
    :type filename: str
    :rtype: str
    """
    mime_types = dict(
        txt='text/plain',
        htm='text/html',
        html='text/html',
        php='text/html',
        css='text/css',
        js='application/javascript',
        json='application/json',
        xml='application/xml',
        swf='application/x-shockwave-flash',
        flv='video/x-flv',

        # images
        png='image/png',
        jpe='image/jpeg',
        jpeg='image/jpeg',
        jpg='image/jpeg',
        gif='image/gif',
        bmp='image/bmp',
        ico='image/vnd.microsoft.icon',
        tiff='image/tiff',
        tif='image/tiff',
        svg='image/svg+xml',
        svgz='image/svg+xml',

        # archives
        zip='application/zip',
        rar='application/x-rar-compressed',
        exe='application/x-msdownload',
        msi='application/x-msdownload',
        cab='application/vnd.ms-cab-compressed',

        # audio/video
        mp3='audio/mpeg',
        ogg='audio/ogg',
        qt='video/quicktime',
        mov='video/quicktime',

        # adobe
        pdf='application/pdf',
        psd='image/vnd.adobe.photoshop',
        ai='application/postscript',
        eps='application/postscript',
        ps='application/postscript',

        # ms office
        doc='application/msword',
        rtf='application/rtf',
        xls='application/vnd.ms-excel',
        ppt='application/vnd.ms-powerpoint',

        # open office
        odt='application/vnd.oasis.opendocument.text',
        ods='application/vnd.oasis.opendocument.spreadsheet',
    )

    ext = os.path.splitext(filename)[1][1:].lower()
    if ext in mime_types:
        return mime_types[ext]
    else:
        return 'application/octet-stream'

def sub(x):
    """
    For substituting the <?php?> require tags with the inner content of the required pages.
    We are actually simulating here the behaviour of an Apache server, since the webpages already
    use PHP, and we don't want to change the infrastructure.
    So we give them what they need in the same framework they work on.
    """
    with open("web/" + x.group(1), "r") as f:
        return f.read()

def get_static(path):
    if (path == "/"):
        return get_static("/index.html")

    p = os.path.abspath(os.path.join(
        (_settings["static_files"] if "static_files" in _settings.keys() else "static/"),
        path[1:].split("?")[0].split("#")[0]
    ))

    if os.path.isdir(p):
        return get_static(os.path.join(p, "index.html"))

    if os.path.exists(p):
        if ".html" in p:
            with io.open(p, mode="r", encoding="utf-8") as f:
                page = f.read() 
            while re.findall("<\?php.+?require\(\"(.+?)\"\);.+?\?>", page):
                page = re.sub("<\?php.+?require\(\"(.+?)\"\);.+?\?>", sub, page)
            page = bytes(page, "utf-8")
        else:
            with open(p, "rb") as f:
                page = f.read()

        mime = mime_content_type(p)

        return page, mime

    return None, None

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

        else:
            page, mime = get_static(self.path)
            if page == None:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(bytes("404 Not Found", "utf-8"))
            else:
                self.send_response(200)
                self.send_header("Content-Type", mime)
                self.end_headers()
                self.wfile.write(page)

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
        
        else: 
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes("404 Not Found", "utf-8"))


def handler(url, method = "GET"):
    global _get_handlers, _post_handlers
    def handler_decorator(func):
        global handlers
        (_get_handlers if method.upper() == "GET" else _post_handlers)[url] = func
        return func
    return handler_decorator

def run(addr, settings = {}):
    global _settings
    _settings = settings 

    httpd = ThreadedHTTPServer(addr, RequestHandler)
    thread = threading.Thread(target=httpd.serve_forever)
    thread.start()
    return thread, httpd