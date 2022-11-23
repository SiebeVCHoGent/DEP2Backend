from fastapi import APIRouter
from starlette import status

from app.main.services import kmoservice

router = APIRouter()


@router.get("/kmo/{ondernemingsnummer}")
def get_kmo(ondernemingsnummer: str):
    return status.HTTP_501_NOT_IMPLEMENTED


@router.get("/kmos")
def search_kmos(search: str):
    """
    Search a kmo in the database
    :param search: Query param search string
    :return: All the found kmos
    """
    return status.HTTP_501_NOT_IMPLEMENTED
