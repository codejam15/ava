from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from src.config import settings as s
from src.middlewares import register_middlewares


@asynccontextmanager
async def lifespan(app: FastAPI):
    # NOTE: This is where you can add your own startup logic.👇
    try:
        ...
        yield
    finally:
        ...


def create_app():
    app = FastAPI(
        title="Teacher Craft API",
        description="Backend for the Teacher Craft application",
        version=s.VERSION,
        docs_url=f"{s.API_PREFIX}/docs",
        openapi_url=f"{s.API_PREFIX}/openapi.json",
        lifespan=lifespan,
    )

    register_middlewares(app)

    # Register routers here.

    return app
