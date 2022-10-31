import ulid

from app.main.common.exceptions import DBException
from app.main.config import db


def add_searchterm(term, parent = None):
    try:
        id = ulid.ulid()
        db.session.add(db.Searchterm(id=id, term=term, parent=parent))
        db.session.commit()
        return {"id": id, "term": term, "parent": parent}
    except Exception as e:
        raise DBException(f'Error while adding searchterm to database {str(e)}')


def get_term_id(term: str):
    term_db = db.session.query(db.Searchterm).filter(db.Searchterm.term == term).first()
    if term_db is None:
        raise ValueError(f'This term does not exist. "{term}"')
    return term_db.id

def get_all_terms():
    terms = db.session.query(db.Searchterm).all()
    return terms


def delete_searchterm(id):
    db.session.query(db.Searchterm).filter(db.Searchterm.id == id).delete()
    db.session.commit()
    return True