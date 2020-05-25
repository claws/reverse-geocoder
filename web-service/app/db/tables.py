from sqlalchemy import (
    BigInteger,
    Column,
    Float,
    Integer,
    MetaData,
    String,
    Table,
)
from geoalchemy2 import Geography


metadata = MetaData()


# This table must match the shape file data imported into the database
countries = Table(
    "countries",
    metadata,
    Column("gid", Integer, primary_key=True),
    Column("fips", String(2)),
    Column("iso2", String(2)),
    Column("iso3", String(3)),
    Column("un", Integer),
    Column("name", String(50)),
    Column("area", Integer),
    Column("pop2005", BigInteger),
    Column("region", Integer),
    Column("subregion", Integer),
    Column("lon", Float),
    Column("lat", Float),
    Column("geog", Geography("MULTIPOLYGON", srid=4326)),
)
