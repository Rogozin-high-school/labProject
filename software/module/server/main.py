from http.server import BaseHTTPRequestHandler, HTTPServer

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        php = "<?php echo 'hello world'; ?>"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes(open("a.php", "r").read(), "utf-8"))
        self.wfile.close()

httpd = HTTPServer(("", 8080), RequestHandler)
httpd.serve_forever()