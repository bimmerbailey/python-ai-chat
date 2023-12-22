from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.logging import setup_fastapi, setup_logging
from app.config.settings import AppSettings, get_app_settings
from app.database.init_db import close_mongo_connection, connect_to_mongo
from app.dependencies.session import close_redis_client, init_redis_client
from app.routes import auth_ui, dashboard_ui, auth_api, users_api, upload_api, chat_api, ingest_api


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_client = await connect_to_mongo()
    redis_client = await init_redis_client()
    yield
    await close_mongo_connection(db_client)
    await close_redis_client(redis_client)


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
    fast_app.include_router(auth_ui)
    fast_app.include_router(dashboard_ui)
    fast_app.include_router(auth_api)
    fast_app.include_router(users_api)
    fast_app.include_router(upload_api)
    fast_app.include_router(ingest_api)
    fast_app.include_router(chat_api)

    return fast_app
