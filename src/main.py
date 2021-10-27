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
import random
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

PARENT = os.path.dirname(os.path.realpath(__file__))


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("content-type", "text/html")
        self.end_headers()

        if "wrong" in self.path:
            with open(os.path.join(PARENT, "wrong.html"), "r") as f:
                self.wfile.write(f.read().encode())

        else:
            vocab = load_vocab()
            words = random.sample(list(vocab.keys()), 4)
            if random.random() < 0.5:
                prompt = vocab[words[0]]
                correct = words[0]
                wrong = words[1:]
            else:
                prompt = words[0]
                correct = vocab[words[0]]
                wrong = [vocab[i] for i in words[1:]]

            self.wfile.write(format_doc(prompt, correct, wrong).encode())


def load_vocab():
    data = {}
    for fname in os.listdir(PARENT):
        if "vocab" in fname and fname.endswith(".json"):
            with open(os.path.join(PARENT, "vocab.json"), "r") as fp:
                data = {**data, **json.load(fp)}

    return data


def format_doc(prompt, correct, wrong):
    with open(os.path.join(PARENT, "template.html"), "r") as f:
        template = f.read()

    correct = f"<a href=\"/\">{correct}</a>"
    wrong = [f"<a href=\"/wrong\">{i}</a>" for i in wrong]
    args = [correct, *wrong]
    random.shuffle(args)

    return template.format(prompt, *args)


def main():
    server = HTTPServer(("", 8080), Handler)
    server.serve_forever()


main()
