from fastapi import APIRouter
from starlette import status

from app.main.services import kmoservice

router = APIRouter()


@router.get("/kmo/{ondernemingsnummer}")
def get_kmo(ondernemingsnummer: str):
    return {"kmo": kmoservice.get_kmo(ondernemingsnummer)}


@router.get("/kmos")
def search_kmos(search: str):
    """
    Search a kmo in the database
    :param search: Query param search string
    :return: All the found kmos
    """
    return {"kmo": kmoservice.search_kmos(search)}

