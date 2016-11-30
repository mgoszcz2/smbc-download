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
