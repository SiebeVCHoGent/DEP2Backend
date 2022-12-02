from fastapi import APIRouter
from starlette.authentication import AuthenticationError, requires
from starlette.requests import Request

from app.main.model.user import User
from app.main.services import authservice

router = APIRouter()


@router.post('/login')
def login(login_data: dict):
    try:
        email = login_data['email']
        password = login_data['password']
    except KeyError:
        raise AuthenticationError('Email and/or password are incorrect.')

    return {"token": authservice.login(email, password)}


@router.post('/register')
def register(register_data: dict):
    try:
        email = register_data['email']
        password = register_data['password']
        naam = register_data['naam']
        voornaam = register_data['voornaam']
    except KeyError as e:
        raise AuthenticationError(f'The {str(e)} field is required for registration.')

    user = User(email=email, password=password, achternaam=naam, voornaam=voornaam)
    return {"token": authservice.register(user)}


@router.patch('/user/{user_id}/role/{role}')
@requires(['admin'])
def update_roles(request: Request, user_id: str, role: str):
    return authservice.update_roles(user_id, role).get_jwt_data()