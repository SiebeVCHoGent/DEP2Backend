from fastapi import FastAPI

from app.main.routers import kmo

app = FastAPI()

app.include_router(kmo.router)

@app.get('/')
def version():
    return {
        'Info': 'Data Engineering Project II: Backend',
        'Version': '0.0.1'
    }
