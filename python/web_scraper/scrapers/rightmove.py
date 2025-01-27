from datetime import datetime
import hashlib
import json
from bs4 import BeautifulSoup
import requests
from common.models import Coordinates, PropertySale
from common.util import coordinates_to_bng
from web_scraper.scrapers.base import (
    BaseScraper,
    ScrapingNetworkError,
    ScrapingParsingError,
)


# TODO: scrape multiple pages with '?pageNumber=2'
class RightmoveScraper(BaseScraper):
    def scrape(self, outward_code: str) -> list[PropertySale]:
        url = f"https://www.rightmove.co.uk/house-prices/{outward_code}.html"
        response = requests.get(url)

        if response.status_code != 200:
            raise ScrapingNetworkError(
                "Rightmove bad response code: {}".format(response.status_code)
            )

        data = self._parse_property_data_from_xml(response.text)
        return self._parse_json_into_sales(data)

    def _parse_property_data_from_xml(self, content: str) -> dict:
        soup = BeautifulSoup(content, features="html.parser")
        matching_tag = 'window.__staticRouterHydrationData = JSON.parse("'

        # look for the script tag with the json content, strip the containing javascript away
        data = None
        for i in soup.find_all("script"):
            if i.string and i.string.startswith(matching_tag):
                json_str = i.string[len(matching_tag) : -3]
                json_str = json_str.replace("\\", "")
                data = json.loads(json_str)
                break

        if not data:
            raise ScrapingParsingError(
                "Could not find expected property data within page content."
            )

        try:
            return data["loaderData"]["property-search-by-location"]
        except:
            raise ScrapingParsingError(
                "Json property data did not have expected structure."
            )

    def _parse_json_into_sales(self, data: dict) -> list[PropertySale]:
        sales: list[PropertySale] = []

        for x in data["properties"]:
            last_txn = x["transactions"][0]
            number = x["address"].split(", ")[0]
            postcode = x["address"].split(", ")[-1][len("Greater London ") :]
            short_address = f"{number}, {postcode}"
            hash_id = hashlib.md5(short_address.encode()).hexdigest()[:16]

            bng_easting, bng_northing = coordinates_to_bng(
                x["location"]["lat"], x["location"]["lng"]
            )
            sales.append(
                PropertySale(
                    id=hash_id,
                    short_address=short_address,
                    address=x["address"],
                    sell_date=datetime.strptime(
                        last_txn["dateSold"], "%d %b %Y"
                    ).date(),
                    price_gbp=int(
                        last_txn["displayPrice"][1:].replace(",", "")
                    ),  # strip £6,000 -> 6000
                    bedroom_count=x["bedrooms"],
                    property_type=x["propertyType"],
                    location=Coordinates(
                        lat=x["location"]["lat"],
                        lon=x["location"]["lng"],
                        bng_easting=bng_easting,
                        bng_northing=bng_northing,
                    ),
                    new_build=last_txn["newBuild"],
                )
            )

        return sales
