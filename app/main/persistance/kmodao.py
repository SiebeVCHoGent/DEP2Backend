from sqlalchemy import desc
from sqlalchemy.orm import aliased

from app.main.common.exceptions import DBException
from app.main.config import db
from app.main.persistance import scoredao


def get_full_kmo(ondernemingsnummer: str):
    try:
        s1 = aliased(db.Sector, name="Sector")
        s2 = aliased(db.Sector, name="Hoofdsector")

        kmo = db.session.query(db.Kmo, db.Gemeente, s1, s2).join(db.Gemeente)\
            .join(s1, db.Kmo.sector == s1.code, isouter=True)\
            .join(s2, s1.superparent == s2.code, isouter=True)\
            .filter(db.Kmo.ondernemingsnummer == ondernemingsnummer).first()

        if kmo is None:
            raise ValueError(f'This kmo does not exist. "{ondernemingsnummer}"')

        kmo = dict(kmo)
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
        kmos = db.session.query(db.Kmo).filter(db.Kmo.naam.ilike(f'%{search}%')).limit(10).all()
        return kmos
    except Exception as e:
        db.session.rollback()
        raise DBException(f'Error while searching kmos from database {str(e)}')