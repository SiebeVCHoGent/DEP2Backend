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


@router.get('/score/ranking/{jaar}/sector')
def get_score_ranking_sector(jaar: int, limit: int = 100):
    return {"sector": termservice.get_score_ranking_sector(jaar, limit)}


@router.get('/score/ranking/{jaar}/hoofdsector')
def get_score_ranking_hoofdsector(jaar: int, limit: int = 100):
    return {"hoofdsector": termservice.get_score_ranking_hoofdsector(jaar, limit)}


@router.get('/score/ranking/{jaar}/sector/{sector}')
def get_score_ranking_sector_kmo(sector: str, jaar: int, limit: int = 15):
    return {"kmos": termservice.get_score_ranking_sector_kmo(sector, jaar, limit)}


@router.get('/score/ranking/{jaar}/hoofdsector/{hoofdsector}')
def get_score_ranking_hoofdsector_kmo(hoofdsector: str, jaar: int, limit: int = 15):
    return {"kmos": termservice.get_score_ranking_hoofdsector_kmo(hoofdsector, jaar, limit)}