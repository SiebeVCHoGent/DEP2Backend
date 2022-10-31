from app.main.config import db
from app.main.model.gemeente import Gemeente
from app.main.model.kmo import Kmo
from app.main.model.sector import Sector
from app.main.model.verslag import Verslag
from app.main.persistance.persistance import data_to_object, add_prefix_to_dict_keys


def get_full_kmo(ondernemingsnummer: str):
    # get kmo from database
    kmo, sector, gemeente = db.session.query(db.Kmo, db.Sector, db.Gemeente).join(db.Verslag).join(db.Gemeente).join(db.Sector).filter(db.Kmo.ondernemingsnummer == ondernemingsnummer).first()
    #get alle verslagen
    verslagen = get_verslagen(ondernemingsnummer)
    kmo = Kmo(**vars(kmo), sector=Sector(**vars(sector)), gemeente=Gemeente(**vars(gemeente)), verslagen=verslagen)
    # convert to object
    return kmo


def get_verslagen(ondernemingsnummer: str):
    verslagen = db.session.query(db.Verslag, db.Jaarverslag, db.Website).join(db.Jaarverslag)\
        .filter(db.Verslag.ondernemingsnummer == ondernemingsnummer).all()
    verslagen_model = []
    for verslag, jaarverslag, website in verslagen:
        jaarverslag = add_prefix_to_dict_keys(vars(jaarverslag), "jaarverslag")
        website = add_prefix_to_dict_keys(vars(website), "website")
        verslag = Verslag(**vars(verslag), **jaarverslag, **website)
        verslagen_model.append(verslag)
    return verslagen_model