from datetime import date
from enum import Enum

from pydantic import BaseModel


class PropertyType(str, Enum):
    FLAT = "FLAT"
    TERRACED = "TERRACED"
    SEMI_DETACHED = "SEMI_DETACHED"
    DETACHED = "DETACHED"


class Coordinates(BaseModel):
    lat: float
    lon: float


class PropertySale(BaseModel):
    id: str
    short_address: str
    address: str
    sell_date: date
    price_gbp: int
    bedroom_count: int | None
    property_type: PropertyType
    location: Coordinates
    new_build: bool
