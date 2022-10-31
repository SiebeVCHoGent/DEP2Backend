from fastapi import APIRouter
from starlette.authentication import requires
from starlette.requests import Request

from app.main.services import termservice

router = APIRouter()


@router.post("/searchterm/{term}")
@requires(["moderator"])
def add_searchterm(request: Request, term: str):
    return termservice.add_searchterm(term)


@router.get("/searchterms")
@requires(["moderator"])
def get_all_terms(request: Request):
    return termservice.get_all_terms()


@router.delete("/searchterm/{term_id}")
@requires(["moderator"])
def add_searchterm(request: Request, term_id: str):
    termservice.delete_searchterm(term_id)
    return termservice.get_all_terms()
