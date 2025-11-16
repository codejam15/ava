from contextlib import asynccontextmanager

from fastapi import FastAPI

import src.routes as r
from src.bot.main import client
from src.config import settings as s
from src.middlewares import register_middlewares


@asynccontextmanager
async def lifespan(app: FastAPI):
    # NOTE: This is where you can add your own startup logic.👇
    try:
        print("Starting up the Discord bot...")
        # client.run(s.BOT_TOKEN)
        yield
    finally:
        ...


def create_app():
    app = FastAPI(
        title="AVA (Agile Virtual Assistant)",
        description="An AI-powered virtual assistant designed to enhance productivity and streamline tasks.",
        version=s.VERSION,
        docs_url=f"{s.API_PREFIX}/docs",
        openapi_url=f"{s.API_PREFIX}/openapi.json",
        lifespan=lifespan,
    )

    register_middlewares(app)

    # Register routers here.
    app.include_router(r.router, prefix=f"{s.API_PREFIX}", tags=["processing"])

    return app
