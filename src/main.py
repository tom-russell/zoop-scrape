from scrapers.zoopla import ZooplaScraper


sales = ZooplaScraper().scrape("E8")

for p in sales:
    print(p)
