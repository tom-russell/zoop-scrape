from scrapers.rightmove import RightmoveScraper
import sqlite3

from db import UnexpectedDBError, PropertySaleTable, init_db
from scrapers.base import BaseScraper, ScrapingError
from util import london_outward_codes
import time

REQUEST_DELAY_S = 1


def scrape_and_insert(
    outward_code: str, table: PropertySaleTable, scraper: BaseScraper
) -> tuple[bool, int]:
    """Scrape data using the given Do X and return a list.
    Returns two arguments:
        - bool - true if the operation was successful, false if it failed at any stage
        - int  - the number of records created during the operation"""
    try:
        sales = scraper.scrape(outward_code)
    except ScrapingError as e:
        print(f"FAILED SCRAPING DATA! {str(e)}")
        return False, 0
    try:
        table.insert_all(sales, raise_if_exists=False)
        return (True, len(sales))
    except UnexpectedDBError as e:
        print(f"FAILED INSERTING RECORDS! {str(e)}")
        # TODO: not strictly correct, some records may have successfully inserted
        return (False, 0)


if __name__ == "__main__":
    scraper = RightmoveScraper()
    connection = init_db()
    table = PropertySaleTable(connection)

    total = len(london_outward_codes())
    failed_codes = 0
    successful_records = 0

    for i, code in enumerate(london_outward_codes()):
        time.sleep(REQUEST_DELAY_S)
        print(f"scraping postcode... {code} - {i+1}/{total}")
        success, insert_count = scrape_and_insert(code, table, scraper)
        failed_codes += 1 if not success else 0
        successful_records += insert_count

    print(f"Scrape complete!")
    print(f"{total - failed_codes} / {total} area codes scraped.")
