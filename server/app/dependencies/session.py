import structlog
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import RedisDsn
from redis.asyncio import Redis

from app.config.settings import (
    RedisSettings,
    get_redis_settings,
    AppSettings,
    get_app_settings,
)

logger = structlog.get_logger(__name__)


class CookieAuth(OAuth2PasswordBearer):
    settings: AppSettings

    def __init__(
        self, token_url: str, settings: AppSettings = Depends(get_app_settings)
    ):
        super().__init__(tokenUrl=token_url)
        self.settings = settings

    async def __call__(self, request: Request) -> str | None:
        authorization = request.cookies.get(self.settings.cookie_name, None)
        if not authorization:
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                )
            else:
                return None
        return authorization


def init_redis_client(redis: RedisSettings = get_redis_settings()) -> Redis:
    logger.info("Connecting to Redis...", db=redis.dsn)
    client = Redis.from_url(str(redis.dsn))
    logger.info("Connected to Redis!")
    return client


async def close_redis_client(client: Redis):
    logger.info("Closing connection to Redis...")
    await client.close()
    logger.info("Connection closed!")


class RedisClient:
    _client: Redis

    def __init__(self, settings: RedisSettings = get_redis_settings()):
        self._client = Redis.from_url(str(settings.dsn))
        logger.info("Connected to Redis!")

    async def close(self):
        logger.info("Closing connection to Redis...")
        await self._client.aclose()
        logger.info("Connection closed!")

    def __call__(self) -> Redis:
        return self.client

    @property
    def client(self):
        return self._client
