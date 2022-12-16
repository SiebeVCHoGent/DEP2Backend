from operator import and_

from sqlalchemy import desc, func
from sqlalchemy.orm import aliased

from app.main.common.exceptions import DBException
from app.main.config import db
from app.main.model import verslag
from app.main.persistance import scoredao


def get_full_kmo(ondernemingsnummer: str):
    try:
        s1 = aliased(db.Sector2, name="Sector")
        s2 = aliased(db.Sector2, name="Hoofdsector")

        kmo = db.session.query(*[c.label(f"kmo-{c.name}") for c in db.Kmo2.columns], *[c.label(f"gemeente-{c.name}") for c in db.Gemeente2.columns],
                               *[c.label(f"sector-{c.name}") for c in s1.columns], *[c.label(f"hoofdsector-{c.name}") for c in s2.columns],
                               *[c.label(f"verslag-{c.name}") for c in db.Verslag2.columns], db.Website2.c.url.label("verslag-website_url"), db.Jaarverslag2.c.url.label("verslag-jaarverslag_url"),
            func.avg(db.Score2.c.website_score).label("website_score"),
            func.avg(db.Score2.c.jaarverslag_score).label("jaarverslag_score"),
            func.avg((db.Score2.c.website_score + db.Score2.c.jaarverslag_score)/2).label("total_score"),
            )\
        .select_from(db.Kmo2)\
        .join(db.Gemeente2, db.Gemeente2.c.postcode == db.Kmo2.c.postcode)\
        .join(s1, s1.c.code == db.Kmo2.c.sector)\
        .join(s2, s2.c.code == s1.c.superparent) \
        .join(db.Verslag2, and_(db.Verslag2.c.ondernemingsnummer == db.Kmo2.c.ondernemingsnummer,
                               db.Verslag2.c.jaar == db.session.query(db.Verslag.jaar).filter(db.Verslag.ondernemingsnummer == db.Kmo2.c.ondernemingsnummer).as_scalar())
        )\
        .join(db.Website2, db.Website2.c.verslag == db.Verslag2.c.id) \
        .join(db.Jaarverslag2, db.Jaarverslag2.c.verslag == db.Verslag2.c.id) \
        .join(db.Score2, db.Score2.c.verslag_id == db.Verslag2.c.id)\
        .filter(db.Kmo2.c.ondernemingsnummer == ondernemingsnummer)\
        .group_by(db.Verslag2.c.id, *[col for col in db.Kmo2.columns], *[col for col in db.Gemeente2.columns], *[col for col in s1.columns], *[col for col in s2.columns], db.Website2.c.url, db.Jaarverslag2.c.url).first()

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