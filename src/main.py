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
import random
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

PARENT = os.path.dirname(os.path.abspath(__file__))
VOCAB_DIR = os.path.join(PARENT, "..", "words")


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = os.path.abspath(self.path.split("?")[0])
        try:
            args = {k: v for k, v in [x.split("=") for x in self.path.split("?")[1].split("&")]}
        except IndexError:
            args = {}

        if path == "/":
            self.send_200(format_doc(load_doc("html/index.html"), load_doc("html/head.html")))
        elif path == "/style.css":
            self.send_200(load_doc("css/style.css"), ctype="text/css")
        elif path == "/multchoice":
            prompt, correct, wrong = pick_words(load_vocab())
            correct_html = f"<a href=\"/multchoice\">{correct}</a>"
            wrong_html = [f"<a href=\"/wrong?correct={correct}\">{i}</a>" for i in wrong]
            words = [correct_html, *wrong_html]
            random.shuffle(words)
            self.send_200(format_doc(load_doc("html/multchoice.html"), load_doc("html/head.html"), prompt, *words))
        else:
            self.send_404()

    def send_404(self):
        self.send_response(404)
        self.send_header("content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<h1>404</h1>")

    def send_200(self, data, ctype="text/html"):
        self.send_response(200)
        self.send_header("content-type", ctype)
        self.end_headers()
        self.wfile.write(data.encode())


def load_vocab():
    data = {}
    for fname in os.listdir(VOCAB_DIR):
        if fname.endswith(".json"):
            with open(os.path.join(VOCAB_DIR, fname), "r") as fp:
                data = {**data, **json.load(fp)}

    return data

def pick_words(vocab):
    words = random.sample(list(vocab.keys()), 4)
    if random.random() < 0.5:
        prompt = vocab[words[0]]
        correct = words[0]
        wrong = words[1:]
    else:
        prompt = words[0]
        correct = vocab[words[0]]
        wrong = [vocab[i] for i in words[1:]]

    return (prompt, correct, wrong)

def load_doc(path):
    with open(os.path.join(PARENT, path), "r") as fp:
        return fp.read()

def format_doc(doc, *args):
    args = list(args)
    final = ""
    for line in doc.split("\n"):
        if "FORMAT" in line:
            line = args.pop(0)
        final += line + "\n"

    return final


def main():
    port = 80 if len(sys.argv) == 1 else int(sys.argv[1])
    server = HTTPServer(("", port), RequestHandler)
    server.serve_forever()


main()
