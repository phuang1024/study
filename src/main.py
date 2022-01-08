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
import string
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

PARENT = os.path.dirname(os.path.abspath(__file__))
VOCAB_DIR = os.path.join(PARENT, "..", "words")

ASCII_ENCODE = "abcdefghijklmnop"

SPECIAL_CHARS = {
    "A'": "&Aacute;",
    "a'": "&aacute;",
    "E'": "&Eacute;",
    "e'": "&eacute;",
    "I'": "&Iacute;",
    "i'": "&iacute;",
    "O'": "&Oacute;",
    "o'": "&oacute;",
    "U'": "&Uacute;",
    "u'": "&uacute;",

    "N~": "&Ntilde;",
    "n~": "&ntilde;",
}


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = os.path.abspath(self.path.split("?")[0])
        try:
            args = {k: v for k, v in [x.split("=") for x in self.path.split("?")[1].split("&")]}
        except IndexError:
            args = {}

        if path == "/":
            self.send_200(load_doc("html/index.html"))
        elif path == "/style.css":
            self.send_200(load_doc("css/style.css"), ctype="text/css")
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


def encode_ascii(data):
    encoded = []

    for byte in data.encode():
        encoded.append(ASCII_ENCODE[byte & 0x0F])
        encoded.append(ASCII_ENCODE[(byte & 0xF0) >> 4])

    return "".join(encoded)

def decode_ascii(data):
    decoded = []

    for i in range(0, len(data), 2):
        decoded.append(
            ASCII_ENCODE.index(data[i]) |
            (ASCII_ENCODE.index(data[i+1]) << 4)
        )

    return bytes(decoded).decode()


def repspecial(text):
    """
    Replace with HTML accent characters.
    """
    for k, v in SPECIAL_CHARS.items():
        text = text.replace(k, v)
    return text

def load_vocab(replace_special=True):
    data = {}
    for fname in os.listdir(VOCAB_DIR):
        if fname.endswith(".json"):
            with open(os.path.join(VOCAB_DIR, fname), "r") as fp:
                data = {**data, **json.load(fp)}

    if replace_special:
        new_data = {}
        for k, v in data.items():
            new_data[repspecial(k)] = repspecial(v)
        data = new_data

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

def load_doc(path, add_header=True):
    with open(os.path.join(PARENT, path), "r") as fp:
        data = fp.read()

    if add_header:
        with open(os.path.join(PARENT, "html/head.html"), "r") as fp:
            data = data.replace("{}", fp.read(), 1)

    return data

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
