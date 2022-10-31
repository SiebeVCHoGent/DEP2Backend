import json

from app.main.common.exceptions import DBException
from app.main.config import db
from app.main.model.user import User


def get_user_by_email(email: str):
    try:
        user = db.session.query(db.User).filter(db.User.email == email).first()
        if user is None:
            return None
        user = User.from_db(user)
        return user
    except Exception as e:
        raise DBException(f'Error getting user by email.\n{str(e)}')


def add_user(user: User):
    db_user = db.User(**user.to_db())
    db.session.add(db_user)
    db.session.commit()
    return user


def delete_user(id: str) -> bool:
    try:
        db.session.query(db.User).filter(db.User.id == id).delete()
        db.session.commit()
        return True
    except Exception as e:
        raise DBException(f'Error removing user.\n{str(e)}')


def get_user_by_id(id: str):
    try:
        user = db.session.query(db.User).filter(db.User.id == id).first()
        if user is None:
            return None
        user = User.from_db(user)
        return user
    except Exception as e:
        raise DBException(f'Error getting user by id.\n{str(e)}')


def update_user(user):
    try:
        db.session.merge(db.User(**user.to_db()))
        db.session.commit()
    except Exception as e:
        raise DBException(f'Error updating user.\n{str(e)}')