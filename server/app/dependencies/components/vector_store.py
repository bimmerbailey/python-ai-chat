import typing
from functools import lru_cache

import structlog.stdlib
from fastapi import Depends
from llama_index import VectorStoreIndex
from llama_index.indices.vector_store import VectorIndexRetriever
from llama_index.vector_stores.milvus import MilvusVectorStore
from llama_index.vector_stores.types import VectorStore

from app.config.settings import MilvusSettings, get_milvus_settings
from app.dependencies.base import ContextFilter, SingletonMetaClass

logger = structlog.stdlib.get_logger(__name__)


class VectorStoreComponent(metaclass=SingletonMetaClass):
    vector_store: VectorStore

    def __init__(
        self,
        milvus_settings: typing.Annotated[
            MilvusSettings, Depends()
        ] = get_milvus_settings(),
    ) -> None:
        self.vector_store = typing.cast(
            VectorStore,
            MilvusVectorStore(
                uri=str(milvus_settings.uri),
                **milvus_settings.model_dump(exclude_none=True, exclude={"uri"}),
            ),
        )

    @staticmethod
    def get_retriever(
        index: VectorStoreIndex,
        context_filter: ContextFilter | None = None,
        similarity_top_k: int = 2,
    ) -> VectorIndexRetriever:
        return VectorIndexRetriever(
            index=index,
            similarity_top_k=similarity_top_k,
        )


@lru_cache
def get_vector_store_component() -> VectorStoreComponent:
    return VectorStoreComponent()
