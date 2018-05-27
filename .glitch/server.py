#!/usr/bin/env python3
import time
import threading
import urllib.request

from http.server import BaseHTTPRequestHandler, HTTPServer


MESSAGE = b"PONG"
INTERVAL = 30


class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()

        self.wfile.write(MESSAGE)


def keep_alive(url):
    while True:
        time.sleep(INTERVAL)

        with urllib.request.urlopen(url) as fp:
            assert fp.read() == MESSAGE


if __name__ == "__main__":
    import os

    url = "https://{}.glitch.me".format(os.environ["PROJECT_DOMAIN"])
    thread = threading.Thread(target=keep_alive, args=(url,))
    thread.daemon = True
    thread.start()

    port = int(os.environ["PORT"])
    server = HTTPServer(("", port), RequestHandler)
    server.serve_forever()
