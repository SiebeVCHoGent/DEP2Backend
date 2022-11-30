from sqlalchemy import func, desc

from app.main.common.exceptions import DBException
from app.main.config import db


def get_scores_for_kmo(ondernemingsnummer: str):
    try:
        return db.session.query(db.Verslag, db.Score, db.Searchterm)\
            .join(db.Score, db.Verslag.id == db.Score.verslag_id) \
            .join(db.Searchterm, db.Score.zoekterm_id == db.Searchterm.id) \
            .filter(db.Verslag.ondernemingsnummer == ondernemingsnummer)\
            .all()
    except Exception as e:
        db.session.rollback()
        raise DBException("Error while getting scores for kmo with ondernemingsnummer: " + ondernemingsnummer + str(e))


def get_score_ranking_all(limit=100):
    try:
        return db.session.query(
        func.rank().over(
            order_by=func.sum(db.Score.website_score + db.Score.jaarverslag_score).desc()
        ).label("rank"),
        func.percent_rank().over(
            order_by=func.sum(db.Score.website_score + db.Score.jaarverslag_score).desc()
        ).label("percent_rank"),
        func.sum(
                (db.Score.website_score + db.Score.jaarverslag_score)).label("total_score"),
        db.Kmo.ondernemingsnummer,
        db.Kmo.naam,
        )\
        .join(db.Verslag, db.Verslag.id == db.Score.verslag_id) \
        .join(db.Kmo, db.Kmo.ondernemingsnummer == db.Verslag.ondernemingsnummer) \
        .group_by(db.Score.verslag_id, db.Kmo.ondernemingsnummer, db.Kmo.naam).order_by(desc("total_score"))\
        .limit(limit)\
        .all()
    except Exception as e:
        db.session.rollback()
        raise DBException("Error while getting score ranking all: " + str(e))