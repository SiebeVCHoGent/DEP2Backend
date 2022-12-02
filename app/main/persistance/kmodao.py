from sqlalchemy import desc

from app.main.common.exceptions import DBException
from app.main.config import db
from app.main.persistance import scoredao


def get_full_kmo(ondernemingsnummer: str):
    try:
        kmo = dict(
            db.session.query(db.Kmo, db.Gemeente, db.Sector).join(db.Gemeente).join(db.Sector)\
            .filter(db.Kmo.ondernemingsnummer == ondernemingsnummer).first()
        )
        kmo['verslagen'] = get_verslagen(ondernemingsnummer)
        # get most recent verslag id
        if len(kmo['verslagen']) > 0:
            kmo['score'] = scoredao.get_gemiddelde_scores(kmo['verslagen'][0]["Verslag"].id)
        return kmo
    except Exception as e:
        db.session.rollback()
        raise DBException(f'Error while getting kmo from database {str(e)}')


def get_verslagen(ondernemingsnummer: str):
    try:
        verslagen = db.session.query(db.Verslag, db.Website.url.label("website_url"), db.Jaarverslag.url.label("jaarverslag_url")).filter(db.Verslag.ondernemingsnummer == ondernemingsnummer)\
            .join(db.Jaarverslag).join(db.Website)\
            .order_by(desc(db.Verslag.jaar)).all()
        return verslagen
    except Exception as e:
        db.session.rollback()
        raise DBException(f'Error while getting verslagen from database {str(e)}')


def search_kmos(search: str):
    try:
        kmos = db.session.query(db.Kmo).filter(db.Kmo.naam.match(search)).all()
        return kmos
    except Exception as e:
        db.session.rollback()
        raise DBException(f'Error while searching kmos from database {str(e)}')