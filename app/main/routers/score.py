from fastapi import APIRouter
from starlette.authentication import requires
from starlette.requests import Request

from app.main.services import termservice

router = APIRouter()


@router.get('/kmo/{ondernemingsnummer}/score')
def get_scores_for_kmo(ondernemingsnummer: str):
    return termservice.get_scores_for_kmo(ondernemingsnummer)


@router.get('/score/ranking/{jaar}')
def get_score_ranking_all(jaar: int, limit: int = 100):
    return termservice.get_score_ranking_all(jaar, limit)


@router.post('/score/recalculate/{jaar}')
@requires(['moderator'])
def recalculate_scores(request: Request, jaar: int):
    return termservice.recalculate_scores(jaar)

