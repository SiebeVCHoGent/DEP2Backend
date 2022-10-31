import typing as t

from fastapi import FastAPI
from fastapi_auth_middleware import AuthMiddleware
from starlette import status
from starlette.authentication import AuthenticationError
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.main.model.user import User
from app.main.routers import kmo, auth
from app.main.config import settings
from app.main.services import authservice

app = FastAPI()

app.include_router(kmo.router)
app.include_router(auth.router)


@app.get('/')
def version():
    return {
        'Info': 'Data Engineering Project II: Backend',
        'Version': settings.VERSION
    }

@app.exception_handler(AuthenticationError)
async def unicorn_exception_handler(request: Request, exc: AuthenticationError):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"error": str(exc)},
    )


def verify_auth(auth_header) -> t.Tuple[t.List[str], User]:
    try:
        header = auth_header['Authorization']
        user = User(**authservice.decrypt_jwt(header))
        return user.roles, user
    except Exception:
        raise AuthenticationError('Authentication failed')


app.add_middleware(AuthMiddleware, verify_header=verify_auth, excluded_urls=['/', '/login', '/register'])