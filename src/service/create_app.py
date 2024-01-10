from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from service.api.routes import api_router
from service.front.pages.router import router as front_router


def create_app():

    app = FastAPI()
    app.mount("/static", StaticFiles(directory="src/service/front/static"), name="static")
    app.include_router(api_router)
    app.include_router(front_router)

    return app
