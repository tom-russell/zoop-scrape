import sqlite3

from models import PropertySale


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
    new_build
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""


class UnexpectedDBError(Exception):
    def __init__(self, operation: str, reason: str) -> None:
        self.message = f"Failed DB operation {operation}: {reason}"
        super().__init__(self.message)


class AlreadyExistsDBError(Exception):
    def __init__(self, id: str) -> None:
        self.message = f"Insert failed, record id: [{id}] already exists"
        super().__init__(self.message)


class PropertySaleTable:
    def __init__(self, con: sqlite3.Connection):
        self.conn = con

    def insert(self, p: PropertySale, raise_if_exists: bool = True) -> None:
        cursor = self.conn.cursor()

        try:
            cursor.execute(
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
