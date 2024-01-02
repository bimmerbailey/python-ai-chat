from contextlib import asynccontextmanager

import structlog.stdlib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.logging import setup_fastapi, setup_logging
from app.config.settings import AppSettings, get_app_settings
from app.database.init_db import close_mongo_connection, connect_to_mongo
from app.dependencies.session import RedisClient
from app.routes.auth import router as auth_router
from app.routes.chat import chat_router
from app.routes.ingest import router as ingest_router
from app.routes.upload import router as upload_router
from app.routes.users import router as users_router

logger = structlog.stdlib.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_client = await connect_to_mongo()
    red = RedisClient()
    yield
    await close_mongo_connection(db_client)
    await red.close()


def init_app(app_settings: AppSettings = get_app_settings()):
    setup_logging(json_logs=app_settings.json_logs, log_level=app_settings.log_level)
    fast_app = FastAPI(
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        lifespan=lifespan,
    )

    origins = ["*"]

    fast_app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    setup_fastapi(fast_app)
    fast_app.include_router(auth_router)
    fast_app.include_router(users_router)
    fast_app.include_router(upload_router)
    fast_app.include_router(ingest_router)
    fast_app.include_router(chat_router)

    return fast_app
