import structlog
from fastapi import HTTPException, Request, status, Depends
from fastapi.security import OAuth2PasswordBearer
from redis.asyncio import Redis
from pydantic import RedisDsn

from app.config.settings import (
    app_settings,
    redis_settings,
    RedisSettings,
    get_redis_settings,
)

logger = structlog.get_logger(__name__)


class CookieAuth(OAuth2PasswordBearer):
    def __init__(self, token_url: str):
        super().__init__(tokenUrl=token_url)

    async def __call__(self, request: Request) -> str | None:
        authorization = request.cookies.get(app_settings.cookie_name, None)
        if not authorization:
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                )
            else:
                return None
        return authorization


def init_redis_client(url: RedisDsn = redis_settings.dsn) -> Redis:
    logger.info("Connecting to Redis...", db=url)
    client = Redis.from_url(str(url))
    logger.info("Connected to Redis!")
    return client


async def close_redis_client(client: Redis):
    logger.info("Closing connection to Redis...")
    await client.close()
    logger.info("Connection closed!")


class RedisClient:
    _client: Redis

    def __init__(self, settings: RedisSettings = Depends(get_redis_settings)):
        self._client = init_redis_client(url=settings.redis_url)

    async def close(self):
        await close_redis_client(self._client)

    def __call__(self) -> Redis:
        return self.client

    @property
    def client(self):
        return self._client
