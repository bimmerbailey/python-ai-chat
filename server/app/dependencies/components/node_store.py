from functools import lru_cache

import structlog.stdlib
from llama_index.core.storage.index_store import SimpleIndexStore
from llama_index.core.storage.index_store.types import BaseIndexStore
from llama_index.storage.docstore.redis import RedisDocumentStore
from llama_index.core.storage.docstore import SimpleDocumentStore, BaseDocumentStore
from llama_index.storage.index_store.redis import RedisIndexStore

from app.config.settings import RedisSettings, get_redis_settings

logger = structlog.stdlib.get_logger(__name__)


class NodeStoreComponent:
    index_store: BaseIndexStore
    doc_store: BaseDocumentStore

    def __init__(self, settings: RedisSettings = get_redis_settings()) -> None:
        try:
            self.index_store = RedisIndexStore.from_host_and_port(
                host=settings.host, port=settings.port
            )
        except FileNotFoundError:
            logger.debug("Local index store not found, creating a new one")
            self.index_store = SimpleIndexStore()

        try:
            self.doc_store = RedisDocumentStore.from_host_and_port(
                host=settings.host, port=settings.port
            )
        except FileNotFoundError:
            logger.debug("Local document store not found, creating a new one")
            self.doc_store = SimpleDocumentStore()


@lru_cache
def get_node_store_component() -> NodeStoreComponent:
    return NodeStoreComponent()
