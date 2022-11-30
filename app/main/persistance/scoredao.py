from app.main.common.exceptions import DBException
from app.main.config import db


def get_scores_for_kmo(ondernemingsnummer: str):
    try:
        return db.session.query(db.Verslag, db.Score, db.Searchterm)\
            .join(db.Score, db.Verslag.id == db.Score.verslag_ID) \
            .join(db.Searchterm, db.Score.zoekterm_ID == db.Searchterm.id) \
            .filter(db.Verslag.ondernemingsnummer == ondernemingsnummer)\
            .all()
    except Exception as e:
        db.session.rollback()
        raise DBException("Error while getting scores for kmo with ondernemingsnummer: " + ondernemingsnummer + str(e))