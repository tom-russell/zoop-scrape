import sqlite3

from common.models import Coordinates, PropertySale


INSERT_PROPERTY_SALE_QUERY_STR = """INSERT INTO property_sale (
    id,
    short_address,
    address,
    sell_date,
    price_gbp,
    bedroom_count,
    property_type,
    location_lat,
    location_lon,
    new_build,
    bng_easting,
    bng_northing
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""
SELECT_QUERY_STR = "SELECT * FROM property_sale limit ? OFFSET ?"
UPDATE_QUERY_STR = "UPDATE property_sale SET {} where id = ?"


def init_db() -> sqlite3.Connection:
    return sqlite3.connect("../db/zoop.db")


class UnexpectedDBError(Exception):
    def __init__(self, operation: str, reason: str) -> None:
        self.message = f"Failed DB operation {operation}: {reason}"
        super().__init__(self.message)


class AlreadyExistsDBError(Exception):
    def __init__(self, id: str) -> None:
        self.message = f"Insert failed, record id: [{id}] already exists"
        super().__init__(self.message)


class PropertySaleTable:
    TABLE_NAME = "property_sale"

    def __init__(self, con: sqlite3.Connection):
        self.conn = con

    def deserialise(self, data: list) -> PropertySale:
        return PropertySale(
            id=data[0],
            short_address=data[1],
            address=data[2],
            sell_date=data[3],
            price_gbp=data[4],
            bedroom_count=data[5],
            property_type=data[6],
            location=Coordinates(
                lat=data[7], lon=data[8], bng_easting=data[10], bng_northing=data[11]
            ),
            new_build=data[9],
        )

    def get(self, limit: int = 10, offset: int = 0) -> list[PropertySale]:
        cur = self.conn.cursor()
        res = cur.execute(
            SELECT_QUERY_STR,
            (
                limit,
                offset,
            ),
        )
        data = []
        for x in res.fetchall():
            data.append(self.deserialise(x))
        return data

    def update(self, id, updates: dict) -> None:
        q = UPDATE_QUERY_STR.format(
            ", ".join([f"{col}={val}" for col, val in updates.items()])
        )
        print(q)
        cur = self.conn.cursor()
        res = cur.execute(q, (id,))
        self.conn.commit()

    def insert(self, p: PropertySale, raise_if_exists: bool = True) -> None:
        cur = self.conn.cursor()

        try:
            cur.execute(
                INSERT_PROPERTY_SALE_QUERY_STR,
                (
                    p.id,
                    p.short_address,
                    p.address,
                    p.sell_date,
                    p.price_gbp,
                    p.bedroom_count,
                    p.property_type,
                    p.location.lat,
                    p.location.lon,
                    p.new_build,
                    p.location.bng_easting,
                    p.location.bng_northing,
                ),
            )
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed: property_sale.id" in str(e):
                if raise_if_exists:
                    AlreadyExistsDBError(p.id)
                else:
                    print("Skipping insert, record already exists.")
                    return

            raise UnexpectedDBError("INSERT", f"Integrity error: {e}")

    def insert_all(
        self, records: list[PropertySale], raise_if_exists: bool = True
    ) -> None:
        for r in records:
            self.insert(r, raise_if_exists)
