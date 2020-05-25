from fastapi import APIRouter, Header, Response, status
from app.config import settings


router = APIRouter()


@router.get(
    "/", status_code=status.HTTP_307_TEMPORARY_REDIRECT, include_in_schema=False
)
def root(response: Response, user_agent: str = Header("")) -> None:
    """ Redirect browsers to the documentation and machines to spec """
    browsers = ("Chrome", "Chromium", "Firefox", "MSIE", "Opera", "Safari")
    if any(browser in user_agent for browser in browsers):
        # Redirect human readable
        response.headers["Location"] = f"{settings.api_v1_path}{settings.docs_path}"
    else:
        # Redirect machine
        response.headers["Location"] = f"{settings.api_v1_path}{settings.open_api_path}"


@router.options("/", include_in_schema=False)
async def index_options():
    return {}
