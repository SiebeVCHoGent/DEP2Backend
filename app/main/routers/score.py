from fastapi import APIRouter
from starlette.authentication import requires
from starlette.requests import Request

from app.main.services import termservice

router = APIRouter()


@router.get('/kmo/{ondernemingsnummer}/score')
def get_scores_for_kmo(ondernemingsnummer: str):
    return termservice.get_scores_for_kmo(ondernemingsnummer)


@router.get('/score/ranking')
def get_score_ranking_all(limit: int = 100):
    return termservice.get_score_ranking_all(limit)