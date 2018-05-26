#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer


class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()

        self.wfile.write(b"OK")


if __name__ == "__main__":
    import os

    port = int(os.environ["PORT"])

    server = HTTPServer(("", port), RequestHandler)
    server.serve_forever()
