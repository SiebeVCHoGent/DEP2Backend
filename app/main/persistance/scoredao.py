import pandas as pd
from sqlalchemy import func, desc, text
from sqlalchemy.orm import aliased

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


def get_gemiddelde_scores(verslag_id):
    try:
        return db.session.query(
            func.avg(db.Score.website_score).label("website_score"),
            func.avg(db.Score.jaarverslag_score).label("jaarverslag_score"),
            func.avg((db.Score.website_score + db.Score.jaarverslag_score) /2).label("total_score")
        ).filter(db.Score.verslag_id == verslag_id).first()
    except Exception as e:
        db.session.rollback()
        raise DBException("Error while getting gemiddelde scores: " + str(e))


def get_score_ranking_sector(jaar, limit):
    try:
        s1 = aliased(db.Sector)
        return db.session.query(
            s1.code,
            s1.naam,
            func.avg(db.Score.website_score).label("website_score"),
            func.avg(db.Score.jaarverslag_score).label("jaarverslag_score"),
            func.avg((db.Score.website_score + db.Score.jaarverslag_score) / 2).label("total_score"),
        )\
        .join(db.Verslag, db.Verslag.id == db.Score.verslag_id)\
        .join(db.Kmo, db.Kmo.ondernemingsnummer == db.Verslag.ondernemingsnummer)\
        .join(s1, s1.code == db.Kmo.sector)\
        .where(db.Verslag.jaar == jaar)\
        .group_by(s1.code, s1.naam)\
        .order_by(desc("total_score"))\
        .all()

    except Exception as e:
        db.session.rollback()
        raise DBException("Error while getting scores sector: " + str(e))


def get_score_ranking_hoofdsector(jaar, limit):
    try:
        s1 = aliased(db.Sector)
        s2 = aliased(db.Sector)

        return db.session.query(
            s2.code,
            s2.naam,
            func.avg(db.Score.website_score).label("website_score"),
            func.avg(db.Score.jaarverslag_score).label("jaarverslag_score"),
            func.avg((db.Score.website_score + db.Score.jaarverslag_score) / 2).label("total_score"),
        ) \
            .join(db.Verslag, db.Verslag.id == db.Score.verslag_id) \
            .join(db.Kmo, db.Kmo.ondernemingsnummer == db.Verslag.ondernemingsnummer) \
            .join(s1, s1.code == db.Kmo.sector) \
            .join(s2, s2.code == s1.superparent) \
            .where(db.Verslag.jaar == jaar) \
            .group_by(s2.code, s2.naam) \
            .order_by(desc("total_score")) \
            .all()

    except Exception as e:
        db.session.rollback()
        raise DBException("Error while getting scores hoofdsector: " + str(e))


def get_score_ranking_sector_kmo(sector, jaar, limit):
    try:
        s1 = aliased(db.Sector)
        return db.session.query(
            s1.code,
            s1.naam.label("sector_naam"),
            db.Kmo.ondernemingsnummer,
            db.Kmo.naam,
            func.avg(db.Score.website_score).label("website_score"),
            func.avg(db.Score.jaarverslag_score).label("jaarverslag_score"),
            func.avg((db.Score.website_score + db.Score.jaarverslag_score) / 2).label("total_score"),
        )\
        .join(db.Verslag, db.Verslag.id == db.Score.verslag_id)\
        .join(db.Kmo, db.Kmo.ondernemingsnummer == db.Verslag.ondernemingsnummer)\
        .join(s1, s1.code == db.Kmo.sector)\
        .where(db.Verslag.jaar == jaar)\
        .where(s1.code == sector)\
        .group_by(s1.code, s1.naam, db.Kmo.ondernemingsnummer, db.Kmo.naam)\
        .order_by(desc("total_score"))\
        .limit(limit)\
        .all()
    except Exception as e:
        db.session.rollback()
        raise DBException("Error while getting scores sector kmo: " + str(e))


def get_score_ranking_hoofdsector_kmo(hoofdsector, jaar, limit):
    try:
        s1 = aliased(db.Sector)
        s2 = aliased(db.Sector)
        return db.session.query(
            s2.code,
            s2.naam.label("sector_naam"),
            db.Kmo.ondernemingsnummer,
            db.Kmo.naam,
            db.Gemeente.naam.label("gemeente"),
            func.avg(db.Score.website_score).label("website_score"),
            func.avg(db.Score.jaarverslag_score).label("jaarverslag_score"),
            func.avg((db.Score.website_score + db.Score.jaarverslag_score) / 2).label("total_score"),
        )\
        .join(db.Verslag, db.Verslag.id == db.Score.verslag_id)\
        .join(db.Kmo, db.Kmo.ondernemingsnummer == db.Verslag.ondernemingsnummer)\
        .join(db.Gemeente, db.Gemeente.postcode == db.Kmo.postcode)\
        .join(s1, s1.code == db.Kmo.sector)\
        .join(s2, s2.code == s1.superparent)\
        .where(db.Verslag.jaar == jaar)\
        .where(s2.code == hoofdsector)\
        .group_by(s2.code, s2.naam, db.Kmo.ondernemingsnummer, db.Kmo.naam, db.Gemeente.naam)\
        .order_by(desc("total_score"))\
        .limit(limit)\
        .all()
    except Exception as e:
        db.session.rollback()
        raise DBException("Error while getting scores hoofdsector kmo: " + str(e))


def get_score_ranking_kmo_in_sector(ondernemingsnummer, jaar):
    try:
        # subquery = db.session.query(db.Searchterm.term, db.Kmo.ondernemingsnummer, db.Sector.superparent,
        #                             func.avg((db.Score.website_score + db.Score.jaarverslag_score) / 2).label("score"),
        #                             func.percent_rank().over(
        #                                 partition_by=(db.Searchterm.term, db.Sector.superparent),
        #                                 order_by=func.avg((db.Score.website_score + db.Score.jaarverslag_score) / 2))
        # )\
        # .select_from(db.Score)\
        # .join(db.Searchterm, db.Searchterm.id == db.Score.zoekterm_id)\
        # .join(db.Verslag, db.Verslag.id == db.Score.verslag_id)\
        # .join(db.Kmo, db.Kmo.ondernemingsnummer == db.Verslag.ondernemingsnummer)\
        # .join(db.Sector, db.Sector.code == db.Kmo.sector)\
        # .group_by(
        #     db.Verslag.id,
        #     db.Searchterm.term,
        #     db.Kmo.ondernemingsnummer,
        #     db.Sector.superparent
        # ).subquery()
        #
        # return db.session.query('*')\
        # .select_from(subquery)\
        # .filter(db.Kmo.ondernemingsnummer == ondernemingsnummer).all()

        # return db.session.query(db.Sector).all()

        subquery = db.session.query(
            db.Searchterm.term,
            db.Kmo.ondernemingsnummer,
            db.Sector.superparent,
            (func.sum(db.Score.website_score) + func.sum(db.Score.jaarverslag_score)).label("score"),
            func.percent_rank().over(
                partition_by=[db.Searchterm.term, db.Sector.superparent],
                order_by = (func.sum(db.Score.website_score) + func.sum(db.Score.jaarverslag_score))
                ).label('rank'))\
        .join(
            db.Score,
            db.Searchterm.id == db.Score.zoekterm_id
        ).join(
            db.Verslag,
            db.Verslag.id == db.Score.verslag_id
        ).join(
            db.Kmo,
            db.Kmo.ondernemingsnummer == db.Verslag.ondernemingsnummer
        ).join(
            db.Sector,
            db.Sector.code == db.Kmo.sector
        ).group_by(
            db.Verslag.id,
            db.Searchterm.term,
            db.Kmo.ondernemingsnummer,
            db.Sector.superparent
        ).subquery()

        return db.session.query(subquery).filter(
            subquery.c.ondernemingsnummer == ondernemingsnummer
        ).all()

    except Exception as e:
        db.session.rollback()
        raise DBException("Error while getting scores kmo in sector: " + str(e))


def get_score_history_for_kmo(ondernemingsnummer):
    try:
        return db.session.query(
        db.Verslag.jaar,
        func.avg(
            (db.Score.website_score + db.Score.jaarverslag_score) / 2
        ).label('score')
    )\
    .join(db.Verslag, db.Score.verslag_id == db.Verslag.id)\
    .filter(db.Verslag.ondernemingsnummer == ondernemingsnummer)\
    .group_by(db.Verslag.jaar).all()
    except Exception as e:
        db.session.rollback()
        raise DBException("Error while getting score history for kmo: " + str(e))