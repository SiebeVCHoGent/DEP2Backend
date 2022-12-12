import ulid
from sqlalchemy import asc

from app.main.common.exceptions import DBException
from app.main.config import db


def add_searchterm(term, parent = None):
    try:
        id = ulid.ulid()
        db.session.add(db.Searchterm(id=id, term=term, parent=parent))
        db.session.commit()
        return {"id": id, "term": term, "parent": parent}
    except Exception as e:
        db.session.rollback()
        raise DBException(f'Error while adding searchterm to database {str(e)}')


def get_term_id(term: str):
    try:
        term_db = db.session.query(db.Searchterm).filter(db.Searchterm.term == term).first()
        if term_db is None:
            raise ValueError(f'This term does not exist. "{term}"')
        return term_db.id
    except Exception as e:
        db.session.rollback()
        raise DBException(f'Error while getting term from database {str(e)}')


def get_all_terms():
    try:
        terms = db.session.query(db.Searchterm).all()
        return terms
    except Exception as e:
        db.session.rollback()
        raise DBException(f'Error while getting terms from database {str(e)}')


def delete_searchterm(id):
    try:
        db.session.query(db.Searchterm).filter(db.Searchterm.id == id).delete()
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        raise DBException(f'Error while deleting searchterm from database {str(e)}')


def add_word(term_id, word):
    try:
        word = db.Woord(id=ulid.ulid(), searchterm=term_id, woord=word)
        db.session.add(word)
        db.session.commit()
        return word
    except Exception as e:
        db.session.rollback()
        raise DBException(f'Error while adding word to database {str(e)}')


def delete_word(woord_id: str):
    try:
        db.session.query(db.Woord).filter(db.Woord.id == woord_id).delete()
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        raise DBException(f'Error while deleting woord from database {str(e)}')


def get_words_for_term(term_id: str):
    try:    
        return db.session.query(db.Woord).filter(db.Woord.searchterm == term_id).order_by(db.Woord.woord).all()
    except Exception as e:
        db.session.rollback()
        raise DBException(f'Error while getting words from database {str(e)}')