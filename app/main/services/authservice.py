import logging
from datetime import datetime, timedelta

import bcrypt
from jose import jwt
from starlette.authentication import AuthenticationError

from app.main.config import settings
from app.main.model.user import User
from app.main.persistance import authdao

log = logging.getLogger(__name__)


def __hash_password(password: str):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()


def __compare_password(unhashed: str, hashed: str) -> bool:
    unhashed = unhashed.encode()
    hashed = hashed.encode()
    return bcrypt.checkpw(unhashed, hashed)


def __create_jwt(jwt_data: dict):
    expiry = {"exp": datetime.utcnow() + timedelta(days=50)}
    return jwt.encode({**jwt_data, **expiry}, settings.JWT_TOKEN)


def decrypt_jwt(bearer_token: str):
    return jwt.decode(bearer_token[7:], settings.JWT_TOKEN)


def register(gebruiker: User) -> str:
    try:
        gebruiker = create_user(gebruiker)
        token = __create_jwt(gebruiker.get_jwt_data())
        return token
    except Exception as e:
        print(e)
        log.error('An error occurred while registering.')


def login(email: str, password: str):
    try:
        gebruiker = get_user_by_email(email)
        if not gebruiker:
            raise Exception()

        if not __compare_password(password, gebruiker.password):
            raise Exception()

        token = __create_jwt(gebruiker.get_jwt_data())
        return token
    except Exception:
        raise AuthenticationError('Name and/or password are incorrect.')


def create_user(gebruiker: User):
    user = get_user_by_email(gebruiker.email)
    if user:
        raise AuthenticationError('This email is already in use.')

    gebruiker.password = __hash_password(gebruiker.password)
    return authdao.add_user(gebruiker)


def delete_user(gebruiker_id: str):
    return authdao.delete_user(gebruiker_id)


def get_user_by_email(email: str):
    return authdao.get_user_by_email(email)


def get_user_by_id(id: str):
    return authdao.get_user_by_id(id)


def update_roles(user_id: str, role: str):
    user = get_user_by_id(user_id)
    if user is None:
        raise ValueError('This user does not exist.')

    if role not in user.roles:
        user.roles.append(role)
    else:
        user.roles.remove(role)

    authdao.update_user(user)

    user = dict(User.from_db(user))
    del user['password']
    return user


def search_user(email):
    user = authdao.search_user(email)
    if user is not None:
        user = dict(user)
        del user['password']
        return user
    return user