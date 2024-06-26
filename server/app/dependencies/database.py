import structlog
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.config.settings import MongoSettings, get_mongo_settings
from app.models.users import User

logger = structlog.stdlib.get_logger(__name__)


async def connect_to_mongo(
    settings: MongoSettings = get_mongo_settings(),
) -> AsyncIOMotorClient:
    logger.info("Connecting to MongoDB...")
    kwargs = {
        "username": settings.username,
        "password": settings.password.get_secret_value(),
    }
    client = AsyncIOMotorClient(str(settings.database_url), **kwargs)
    await init_beanie(database=client[settings.name], document_models=[User])
    logger.info("Connected to MongoDB!")
    return client


async def close_mongo_connection(client: AsyncIOMotorClient):
    logger.info("Closing connection to MongoDB...")
    client.close()
    logger.info("Connection closed!")
