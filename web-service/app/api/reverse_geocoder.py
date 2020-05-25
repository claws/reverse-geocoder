from databases import Database
from fastapi import APIRouter, Depends
from app.models import PostionQueryIn, PostionQueryOut
from app.db import get_db, reverse_geocoder


router = APIRouter()


@router.post("/", response_model=PostionQueryOut)
async def query_position_country(
    query_params: PostionQueryIn, database: Database = Depends(get_db),
):
    result = await reverse_geocoder.query(database, query_params)
    d = query_params.dict(by_alias=True)
    d["country"] = dict(result) if result else None
    return PostionQueryOut(**d)
