from fastapi import APIRouter

from app.main.services import kmoservice

router = APIRouter()


@router.get("/kmo/{ondernemingsnummer}")
def get_kmo(ondernemingsnummer: str):
    return kmoservice.get_kmo(ondernemingsnummer)
