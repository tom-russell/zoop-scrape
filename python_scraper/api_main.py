from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

# from db import PropertySaleTable, init_db
from db import init_db
from db import PropertySaleTable
from util import LONDON_BOUNDARY_NE, LONDON_BOUNDARY_SW, coordinates_to_bng
import logging
import time


log = logging.getLogger("uvicorn.error")
app = FastAPI()
connection = init_db()
table = PropertySaleTable(connection)


class PropertySaleResponse(BaseModel):
    id: str
    short_code: str
    price_gbp: int
    bng_coordinate_x: float
    bng_coordinate_y: float


class CoordinateAreaResponse(BaseModel):
    bng_coordinate_x_min: float
    bng_coordinate_y_min: float
    bng_coordinate_x_max: float
    bng_coordinate_y_max: float


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/sales")
async def sales(count: int = 10) -> list[PropertySaleResponse]:
    data = table.get(count)
    # return data
    out = []
    for x in data:
        out.append(
            PropertySaleResponse(
                id=x.id,
                short_code=x.short_address.split(" ")[-2],
                price_gbp=x.price_gbp,
                bng_coordinate_x=x.location.bng_easting,
                bng_coordinate_y=x.location.bng_northing,
            )
        )

    return out


@app.get("/london-coordinates")
async def london_coords() -> CoordinateAreaResponse:
    return CoordinateAreaResponse(
        bng_coordinate_x_min=LONDON_BOUNDARY_SW[0],
        bng_coordinate_y_min=LONDON_BOUNDARY_SW[1],
        bng_coordinate_x_max=LONDON_BOUNDARY_NE[0],
        bng_coordinate_y_max=LONDON_BOUNDARY_NE[1],
    )
