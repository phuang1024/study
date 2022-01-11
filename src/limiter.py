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

import time


class Limiter:
    def __init__(self, limits, vip):
        """
        Handles rate limiting.

        :param limits: List of (req, time) meaning
            at most req requests per time seconds.
        :param vip: List of IPs that are allowed to bypass the limiter.
        """
        self.limits = sorted(limits, key=lambda x: x[1])
        self.vip = vip
        self.reqs = {}

    def _req_valid(self, ip):
        """
        Checks if the request is valid.
        """
        now = time.time()
        for req, t in self.limits:
            if len(self.reqs[ip]) < req:
                continue
            if now - self.reqs[ip][-req] < t:
                return False

        return True

    def request(self, ip):
        if ip in self.vip:
            return True
        if ip not in self.reqs:
            self.reqs[ip] = []
            return True
        if not self._req_valid(ip):
            return False

        now = time.time()
        self.reqs[ip].append(now)
        max_limit = self.limits[-1][1]
        while len(self.reqs[ip]) > 0 and now - self.reqs[ip][0] > max_limit:
            self.reqs[ip].pop(0)

        return True


limiter = Limiter(((300, 300), (3000, 3600)), ())
