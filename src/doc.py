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

import random
import json
from constants import *


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
