from functools import lru_cache
from typing import Annotated

import structlog.stdlib
from llama_index.storage.docstore import (
    BaseDocumentStore,
    RedisDocumentStore,
    SimpleDocumentStore,
)
from llama_index.storage.index_store import RedisIndexStore, SimpleIndexStore
from llama_index.storage.index_store.types import BaseIndexStore
from fastapi import Depends

from app.config.settings import RedisSettings, get_redis_settings
from app.dependencies.base import SingletonMetaClass

logger = structlog.stdlib.get_logger(__name__)


class NodeStoreComponent(metaclass=SingletonMetaClass):
    index_store: BaseIndexStore
    doc_store: BaseDocumentStore

    def __init__(
        self, settings: Annotated[RedisSettings, Depends()] = get_redis_settings()
    ) -> None:
        try:
            # self.index_store = SimpleIndexStore.from_persist_dir(
            #     persist_dir=str(local_data_path)
            # )
            self.index_store = RedisIndexStore.from_host_and_port(
                host=settings.host, port=settings.port
            )
        except FileNotFoundError:
            logger.debug("Local index store not found, creating a new one")
            self.index_store = SimpleIndexStore()

        try:
            # self.doc_store = SimpleDocumentStore.from_persist_dir(
            #     persist_dir=str(local_data_path)
            # )
            self.doc_store = RedisDocumentStore.from_host_and_port(
                host=settings.host, port=settings.port
            )
        except FileNotFoundError:
            logger.debug("Local document store not found, creating a new one")
            self.doc_store = SimpleDocumentStore()


@lru_cache
def get_node_store_component() -> NodeStoreComponent:
    return NodeStoreComponent()
