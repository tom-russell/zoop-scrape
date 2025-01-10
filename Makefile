db_init:
	sqlite3 zoop.db < src/db/migrations/V01__create_property_sale_table.sql

run:
	python src/main.py

freeze:
	pip freeze > requirements.txt