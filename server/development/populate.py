import asyncio
import io
from datetime import datetime, timezone

import structlog
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.config.settings import MongoSettings, get_mongo_settings
from app.dependencies.auth import get_crypt_context
from app.models.users import User

logger: structlog.stdlib.BoundLogger = structlog.getLogger(__name__)


async def connect_db(mongo_settings: MongoSettings = get_mongo_settings()) -> None:
    kwargs = {
        "username": mongo_settings.username,
        "password": mongo_settings.password,
    }
    client = AsyncIOMotorClient(str(mongo_settings.database_url), **kwargs)
    await init_beanie(client[mongo_settings.name], document_models=[User])


async def create_users(crypt_context=get_crypt_context()):
    logger.info("Dropping local Users collection")
    await User.delete_all()

    users = [
        User(
            **{
                "email": "admin@your-app.com",
                "first_name": "admin",
                "password": crypt_context.hash("password"),
                "created_date": datetime.now(tz=timezone.utc),
                "is_admin": True,
            }
        ),
        User(
            **{
                "email": "user@your-app.com",
                "first_name": "user",
                "password": crypt_context.hash("password"),
                "created_date": datetime.now(tz=timezone.utc),
            }
        ),
    ]

    await User.insert_many(users)
    logger.info("Users added")


async def create_dev_data():
    await connect_db()
    await create_users()


if __name__ == "__main__":
    asyncio.run(create_dev_data())
