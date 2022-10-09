from fastapi import FastAPI

from app.main.routers import kmo
from app.main.config import settings

app = FastAPI()

app.include_router(kmo.router)


@app.get('/')
def version():
    return {
        'Info': 'Data Engineering Project II: Backend',
        'Version': settings.VERSION
    }
