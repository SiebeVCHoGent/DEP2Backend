import pandas as pd
from sqlalchemy import func, desc

from app.main.common.exceptions import DBException
from app.main.config import db


def get_all_verslagen():
    try:
        return db.session.query(db.Verslag).all()
    except Exception as e:
        db.session.rollback()
        raise DBException("Error while getting all verslagen: " + str(e))


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


def get_score_ranking_all(jaar: int, limit: int=100):
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
        .where(db.Verslag.jaar == jaar) \
        .limit(limit)\
        .all()
    except Exception as e:
        db.session.rollback()
        raise DBException("Error while getting score ranking all: " + str(e))


def calculate_score(woorden, jaar: int):
    try:
        # build woorden query
        wq = "to_tsquery('dutch', '{}')".format(' | '.join(woorden))

        scores = db.session.execute(f"SELECT v.id, ts_rank(jv.tekst_vector, {wq}), "
                                 f"ts_rank(w.tekst_vector, {wq}) FROM verslag AS v "
                                 "LEFT JOIN jaarverslag AS jv ON jv.verslag = v.id "
                                 "LEFT JOIN website as w ON w.verslag = v.id "
                                 f"WHERE v.jaar = {jaar}").all()
        return scores
    except Exception as e:
        db.session.rollback()
        raise DBException("Error while calculating score: " + str(e))


def scores_to_db(zoekterm_id: str, df: pd.DataFrame):
    try:
        for index, row in df.iterrows():
            db.session.add(db.Score(zoekterm_id=zoekterm_id, jaarverslag_score=row['jaarverslag_score'],
                                      website_score=row['website_score'], verslag_id=row['verslag_id']))
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise DBException("Error while adding scores to database: " + str(e))


def delete_scores_for_year(jaar):
    try:
        db.session.query(db.Score).filter(db.Score.verslag_id.in_(
            db.session.query(db.Verslag.id).filter(db.Verslag.jaar == jaar)))\
            .delete(synchronize_session=False)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise DBException("Error while deleting scores for year: " + str(e))