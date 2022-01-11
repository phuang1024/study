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

import os
from http.server import BaseHTTPRequestHandler
from doc import *


class RequestHandler(BaseHTTPRequestHandler):
    def _get_css_sizes(self):
        mobile = "User-Agent" in self.headers and "Mobile" in self.headers["User-Agent"]

        if mobile:
            return [80, 60, 40]
        else:
            return [36, 24, 18]

    def do_GET(self):
        try:
            from limiter import limiter
            if limiter.request(self.client_address[0]):
                self.do_GET_real()
            else:
                self.send_code(429, "Too many requests")

        except Exception as e:
            print(e)
            self.send_code(500)
    
    def do_GET_real(self):
        path = os.path.abspath(self.path.split("?")[0])
        try:
            args = {k: v for k, v in [x.split("=") for x in self.path.split("?")[1].split("&")]}
        except IndexError:
            args = {}

        if path == "/":
            self.send_200(load_doc("html/index.html"))

        elif path == "/style.css":
            doc = load_doc("css/style.css", add_header=False)
            for size in self._get_css_sizes():
                doc = doc.replace("SIZE", str(size), 1)
            self.send_200(doc, ctype="text/css")

        elif path == "/about":
            self.send_200(load_doc("html/about.html"))

        elif path == "/multchoice":
            prompt, correct, wrong = pick_words(load_vocab())
            prompt_id, correct_id = map(encode_ascii, (prompt, correct))
            base_html = "<a href=\"/multchoice/{2}?prompt={0}&choice={3}&correct={1}\">{4}</a>" \
                .format(prompt_id, correct_id, *"{} {} {}".split())
            correct_html = base_html.format("", prompt_id, correct)
            wrong_html = [base_html.format("wrong", encode_ascii(i), i) for i in wrong]
            words = [correct_html, *wrong_html]
            random.shuffle(words)
            self.send_200(load_doc("html/multchoice.html").format(prompt, *words))

        elif path == "/multchoice/wrong":
            prompt = decode_ascii(args["prompt"])
            correct = decode_ascii(args["correct"])
            choice = decode_ascii(args["choice"])
            self.send_200(load_doc("html/multchoice-wrong.html").format(prompt, correct, choice))

        else:
            self.send_code(404)

    def send_code(self, code, msg=None):
        if msg is None:
            msg = code
        self.send_response(code)
        self.send_header("content-type", "text/html")
        self.end_headers()
        self.wfile.write(f"<h1>{msg}</h1>".encode())

    def send_200(self, data, ctype="text/html"):
        self.send_response(200)
        self.send_header("content-type", ctype)
        self.end_headers()
        self.wfile.write(data.encode())
