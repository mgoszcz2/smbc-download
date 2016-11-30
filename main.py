# smbc-download - Download top 100 comics from smbc
# Copyright (C) 2016 Maciej Goszczycki
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import requests
from bs4 import BeautifulSoup
import os

print("Downloading into smbc/")
smbc = "http://www.smbc-comics.com/comic/"
os.makedirs("smbc", exist_ok=True)
for name in BeautifulSoup(requests.get(smbc + "archive/").text, "html.parser").select("option"):
    if not name["value"]:
        continue
    url = BeautifulSoup(requests.get(smbc + name["value"]).text, "html.parser").select_one("#cc-comic")["src"]
    fname = "smbc/" + name["value"] + os.path.splitext(url)[1]
    if os.path.exists(fname):
        print("Skipping", fname)
    else:
        print("Downloading", fname)
        with open(fname, "wb") as f:
            f.write(requests.get(url).content)
