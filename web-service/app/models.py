import datetime
import enum
from pydantic import BaseModel, Field, constr
from typing import List, Literal, Optional, Tuple, Union


class GeoPoint(BaseModel):
    latitude: float
    longitude: float
    altitude: float = None


class PostionQueryIn(BaseModel):
    location: GeoPoint = Field(
        None, title="Location", description="The location to check"
    )

    class Config:
        schema_extra = {
            "example": {"location": {"latitude": -34.46786, "longitude": 138.56826,},}
        }


class CountryDetails(BaseModel):
    name: str
    iso2: str
    iso3: str


class PostionQueryOut(PostionQueryIn):
    country: CountryDetails = None

    class Config:
        schema_extra = {
            "example": {
                "location": {"latitude": -34.46786, "longitude": 138.56826,},
                "country": {"name": "Australia", "iso2": "AU", "iso3": "AUS",},
            }
        }
