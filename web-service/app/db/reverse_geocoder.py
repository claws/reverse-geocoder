import logging
from databases import Database
from sqlalchemy.sql import select
from geoalchemy2.functions import ST_GeographyFromText, ST_Covers
from app.models import PostionQueryIn, GeoPoint
from app.db.tables import countries
from typing import List, Tuple, Union


logger = logging.getLogger(__name__)

_database = None


async def query(database: Database, payload: PostionQueryIn):
    """ Find whether a point is within a country """
    query = select([countries.c.name, countries.c.iso2, countries.c.iso3])
    # Convert a GeoPoint into a format that can be used in postgis queries
    point = f"POINT({payload.location.longitude} {payload.location.latitude})"
    query = query.where(
        ST_Covers(countries.c.geog, ST_GeographyFromText(f"SRID=4326;{point}"))
    )
    results = await database.fetch_one(query=query)
    return results
