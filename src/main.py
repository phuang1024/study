#
#  Study
#  Simple web app for studying vocabulary.
#  Copyright Patrick Huang 2021
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import sys
import os
from http.server import HTTPServer, BaseHTTPRequestHandler


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = os.path.abspath(self.path.split("?")[0])
        try:
            args = {k: v for k, v in [x.split("=") for x in self.path.split("?")[1].split("&")]}
        except IndexError:
            args = {}

        if path == "/":
            self.send_file("html/index.html")
        elif path == "/style.css":
            self.send_file("css/style.css", "text/css")
        else:
            self.send_404()

    def send_404(self):
        self.send_response(404)
        self.send_header("content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<h1>404</h1>")

    def send_file(self, path, ctype="text/html"):
        with open(path, "rb") as f:
            self.send_response(200)
            self.send_header("content-type", ctype)
            self.end_headers()
            self.wfile.write(f.read())


def main():
    port = 80 if len(sys.argv) == 1 else int(sys.argv[1])
    server = HTTPServer(("", port), RequestHandler)
    server.serve_forever()


main()
