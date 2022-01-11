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
