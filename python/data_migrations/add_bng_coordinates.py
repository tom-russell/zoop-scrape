from db import PropertySaleTable, init_db
from util import coordinates_to_bng


if __name__ == "__main__":
    connection = init_db()
    table = PropertySaleTable(connection)

    limit = 100
    offset = 0
    count = 0
    while True:
        results = table.get(limit=limit, offset=offset)
        count += len(results)
        offset += limit

        for x in results:
            easting, northing = coordinates_to_bng(x.location.lat, x.location.lon)
            table.update(x.id, {"bng_easting": easting, "bng_northing": northing})

        if len(results) == 0:
            break
