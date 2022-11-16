import typing as t

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from fastapi_auth_middleware import AuthMiddleware
from starlette import status
from starlette.authentication import AuthenticationError
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.main.model.user import User
from app.main.routers import kmo, auth, tree
from app.main.config import settings
from app.main.services import authservice

app = FastAPI(docs_url="/docs", redoc_url="/redoc", openapi_url="/")

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="HOGENT - Data Engineering Project",
        version=settings.VERSION,
        description="Data Engineering Project Created for HOGENT. View all the SME's in Flanders and their data.",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://upload.wikimedia.org/wikipedia/commons/1/10/HoGent_Logo.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema
app.openapi = custom_openapi

app.include_router(kmo.router)
app.include_router(auth.router)
app.include_router(tree.router)


@app.exception_handler(AuthenticationError)
async def unicorn_exception_handler(request: Request, exc: AuthenticationError):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"error": str(exc)},
    )


@app.exception_handler(ValueError)
async def unicorn_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error": str(exc)},
    )


@app.exception_handler(Exception)
async def unicorn_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": f"Internal Server Error {str(exc)}"},
    )

def verify_auth(auth_header) -> t.Tuple[t.List[str], User]:
    try:
        header = auth_header['Authorization']
        user = User(**authservice.decrypt_jwt(header))
        return user.roles, user
    except Exception:
        raise AuthenticationError('Authentication failed')

app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.add_middleware(AuthMiddleware, verify_header=verify_auth, excluded_urls=['/', '/login', '/register', '/redoc', '/docs'])