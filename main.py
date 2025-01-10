import requests
import json
import hashlib
from bs4 import BeautifulSoup
from pydantic import BaseModel
from decimal import Decimal
from enum import Enum
from datetime import date, datetime

class PropertyType(str, Enum):
    FLAT = "FLAT"
    TERRACED = "TERRACED"


class Coordinates(BaseModel):
    lat: Decimal
    lng: Decimal


class PropertySale(BaseModel):
    id: str
    short_address: str
    address: str
    sell_date: date
    price_gbp: int
    bedroom_count: int | None
    property_type: PropertyType
    location: Coordinates
    new_build: bool


url = "https://www.rightmove.co.uk/house-prices/e8.html"
response = requests.get(url)
if response.status_code != 200:
    raise RuntimeError("bad response code: {}".format(response.status_code))

soup = BeautifulSoup(response.text, features="html.parser")

tag_match = 'window.__staticRouterHydrationData = JSON.parse("'

data = None
for i in soup.find_all("script"):
    if i.string and i.string.startswith(tag_match):
        json_str = i.string[len(tag_match) : -3]
        json_str = json_str.replace("\\", "")
        data = json.loads(json_str)
        break


sales: list[PropertySale] = []

for x in data["loaderData"]["property-search-by-location"]["properties"]:
    last_txn = x["transactions"][0]
    number = x["address"].split(", ")[0]
    postcode = x["address"].split(", ")[-1][len("Greater London "):]
    short_address = f"{number}, {postcode}"
    hash_id = hashlib.md5(short_address.encode()).hexdigest()[:16]

    sales.append(
        PropertySale(
            id=hashlib.md5(short_address.encode()).hexdigest(),
            short_address=short_address,
            address=x["address"],
            sell_date=datetime.strptime(last_txn["dateSold"], '%d %b %Y').date(),
            price_gbp=int(last_txn["displayPrice"][1:].replace(",","")),  # strip £6,000 -> 6000
            bedroom_count=x["bedrooms"],
            property_type=x["propertyType"],
            location=Coordinates(
                lat=x["location"]["lat"],
                lng=x["location"]["lng"],
            ),
            new_build=last_txn["newBuild"],
        )
    )
