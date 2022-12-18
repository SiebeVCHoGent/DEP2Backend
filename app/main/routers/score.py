import time

from fastapi import APIRouter
from numpy import random
from starlette.authentication import requires
from starlette.requests import Request

from app.main.services import termservice, predictionservice

router = APIRouter()


@router.get('/kmo/{ondernemingsnummer}/score')
def get_scores_for_kmo(ondernemingsnummer: str):
    return termservice.get_scores_for_kmo(ondernemingsnummer)


@router.get('/score/ranking/{jaar}')
def get_score_ranking_all(jaar: int, limit: int = 100):
    return termservice.get_score_ranking_all(jaar, limit)


@router.post('/score/recalculate/{jaar}')
def recalculate_scores(jaar: int):
    return termservice.recalculate_scores(jaar)


@router.get('/score/ranking/{jaar}/sector')
def get_score_ranking_sector(jaar: int, limit: int = 100):
    return {"sector": termservice.get_score_ranking_sector(jaar, limit)}


@router.get('/score/ranking/{jaar}/hoofdsector')
def get_score_ranking_hoofdsector(jaar: int, limit: int = 100):
    return {"hoofdsector": termservice.get_score_ranking_hoofdsector(jaar, limit)}


@router.get('/score/ranking/{jaar}/sector/{sector}')
def get_score_ranking_sector_kmo(sector: str, jaar: int, limit: int = 50):
    return {"kmos": termservice.get_score_ranking_sector_kmo(sector, jaar, limit)}


@router.get('/score/ranking/{jaar}/hoofdsector/{hoofdsector}')
def get_score_ranking_hoofdsector_kmo(hoofdsector: str, jaar: int, limit: int = 50):
    return {"kmos": termservice.get_score_ranking_hoofdsector_kmo(hoofdsector, jaar, limit)}


@router.get('/score/ranking/{jaar}/kmo/{ondernemingsnummer}')
def get_score_ranking_kmo_in_sector(ondernemingsnummer: str, jaar: int):
    return termservice.get_score_ranking_kmo_in_sector(ondernemingsnummer, jaar)


@router.get('/score/kmo/{ondernemingsnummer}/history')
def get_score_history_for_kmo(ondernemingsnummer: str):
    return termservice.get_score_history_for_kmo(ondernemingsnummer)


@router.get('/graph/{jaar}/{ondernemingsnummer}')
def get_graph_data_for_kmo(jaar: int, ondernemingsnummer: str):
    return {
        "sector_percent": termservice.get_score_ranking_kmo_in_sector(ondernemingsnummer, jaar),
        "history": termservice.get_score_history_for_kmo(ondernemingsnummer)
    }


@router.post('/predict')
def predict_score(prediction_data: dict):
    try:
        beursgenoteerd = bool(prediction_data['beursgenoteerd'])
        verstedelijkingsgraad = int(prediction_data['verstedelijkingsgraad'])
        balanstotaal = int(prediction_data['balanstotaal'])
        aantalwerknemers = int(prediction_data['aantalwerknemers'])
        omzet = int(prediction_data['omzet'])
        omzetperwerknemer = int(omzet / aantalwerknemers)
        hoofdsector = str(prediction_data['hoofdsector'])
    except KeyError as e:
        raise Exception(f'The {str(e)} field is required for registration.')

    time.sleep(2)
    return predictionservice.predict(beursgenoteerd, verstedelijkingsgraad, aantalwerknemers, omzet, omzetperwerknemer, balanstotaal, hoofdsector)