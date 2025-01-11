CREATE TABLE IF NOT EXISTS property_sale (
	id TEXT PRIMARY KEY,
   	short_address TEXT NOT NULL,
   	address TEXT NOT NULL,
   	sell_date TEXT NOT NULL,
   	price_gbp INTEGER NOT NULL,
   	bedroom_count INTEGER,
   	property_type TEXT CHECK(property_type IN ('TERRACED', 'FLAT', 'SEMI_DETACHED', 'DETACHED')) NOT NULL,
   	location_lat REAL NOT NULL,
   	location_lon REAL NOT NULL,
   	new_build INTEGER NOT NULL
) WITHOUT ROWID;
