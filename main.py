import requests
import json
from bs4 import BeautifulSoup


url = "https://www.rightmove.co.uk/house-prices/e8.html"
response = requests.get(url)
if response.status_code != 200:
    raise RuntimeError("bad response code: {}".format(response.status_code))

soup = BeautifulSoup(response.text, features="html.parser")

tag_match = "window.__staticRouterHydrationData = JSON.parse(\""

data = None
for i in soup.find_all("script"):
    if i.string and i.string.startswith(tag_match):
        json_str = i.string[len(tag_match):-3]
        json_str = json_str.replace("\\", "")
        print(json_str)

        data = json.loads(json_str)


for x in data["loaderData"]["property-search-by-location"]["properties"]:
    print(x["address"])
