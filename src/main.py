from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from .api.router import router as api_router


def create_app() -> FastAPI:
    app = FastAPI(
        title='fastapi-app',
        redoc_url=None,
        default_response_class=ORJSONResponse,
    )
    app.include_router(api_router)

    return app
