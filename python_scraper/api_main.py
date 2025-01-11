from fastapi import FastAPI

from db import PropertySaleTable, init_db
from models import PropertySale

app = FastAPI()
connection = init_db()
table = PropertySaleTable(connection)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/sales")
async def sales() -> list[PropertySale]:
    data = table.get(10)
    return data
