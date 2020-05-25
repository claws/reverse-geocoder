import logging
from databases import Database
from sqlalchemy import create_engine
from geoalchemy2 import Geography
from app.config import Settings
from typing import List, Tuple, Union
from . import tables
from . import reverse_geocoder


logger = logging.getLogger(__name__)

_database = None


def get_db() -> Database:
    """ Return the database singleton """
    global _database
    if _database is None:
        raise Exception("database has not been configured")
    return _database


def configure(settings: Settings = None) -> Database:
    """ Configure the database singleton """
    global _database
    if _database is not None:
        raise Exception("database has already been configured")
    database = Database(settings.database_dsn, force_rollback=settings.database_test)
    engine = create_engine(settings.database_dsn)
    tables.metadata.create_all(engine)
    _database = database
    return _database
