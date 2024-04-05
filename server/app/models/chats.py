from datetime import datetime, timezone
from typing import Literal

from beanie import Document
from pydantic import BaseModel, Field


class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class Users(Document):
    created_date: datetime = datetime.now(tz=timezone.utc)
    # TODO: Limited length?
    messages: list[Message] = Field(default_factory=list)
