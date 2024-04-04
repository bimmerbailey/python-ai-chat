import typing
from functools import lru_cache

import structlog.stdlib
from fastapi import Depends

from llama_index.core.indices.vector_store import VectorIndexRetriever, VectorStoreIndex
from llama_index.core.vector_stores.types import (
    FilterCondition,
    MetadataFilter,
    MetadataFilters,
    VectorStore,
)
from llama_index.vector_stores.milvus import MilvusVectorStore

from app.config.settings import MilvusSettings, get_milvus_settings
from app.dependencies.base import ContextFilter

logger = structlog.stdlib.get_logger(__name__)


def _doc_id_metadata_filter(
    context_filter: ContextFilter | None,
) -> MetadataFilters:
    filters = MetadataFilters(filters=[], condition=FilterCondition.OR)

    if context_filter is not None and context_filter.docs_ids is not None:
        for doc_id in context_filter.docs_ids:
            filters.filters.append(MetadataFilter(key="doc_id", value=doc_id))

    return filters


class VectorStoreComponent:
    vector_store: VectorStore

    def __init__(
        self,
        milvus_settings: MilvusSettings = get_milvus_settings(),
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
            doc_ids=context_filter.docs_ids if context_filter else None,
            filters=(_doc_id_metadata_filter(context_filter)),
        )

    def close(self) -> None:
        if hasattr(self.vector_store.client, "close"):
            self.vector_store.client.close()


@lru_cache
def get_vector_store_component() -> VectorStoreComponent:
    return VectorStoreComponent()
