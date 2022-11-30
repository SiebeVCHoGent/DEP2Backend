from app.main.config import db


def get_full_kmo(ondernemingsnummer: str):
    kmo = dict(db.session.query(db.Kmo, db.Gemeente, db.Sector).join(db.Gemeente).join(db.Sector)\
        .filter(db.Kmo.ondernemingsnummer == ondernemingsnummer).first())
    kmo['verslagen'] = get_verslagen(ondernemingsnummer)
    return kmo


def get_verslagen(ondernemingsnummer: str):
    verslagen = db.session.query(db.Verslag).filter(db.Verslag.ondernemingsnummer == ondernemingsnummer).all()
    return verslagen


def search_kmos(search: str):
    kmos = db.session.query(db.Kmo).filter(db.Kmo.naam.match(search)).all()
    return kmos