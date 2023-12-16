from typing import Annotated

import structlog.stdlib
from fastapi import Depends
from llama_index import ServiceContext, StorageContext, VectorStoreIndex
from llama_index.chat_engine import ContextChatEngine
from llama_index.chat_engine.types import BaseChatEngine
from llama_index.indices.postprocessor import MetadataReplacementPostProcessor
from llama_index.llm_predictor.utils import stream_chat_response_to_tokens
from llama_index.llms import ChatMessage
from llama_index.types import TokenGen
from pydantic import BaseModel

from app.dependencies.base import ContextFilter, SingletonMetaClass
from app.dependencies.components import (
    EmbeddingComponent,
    LLMComponent,
    NodeStoreComponent,
    VectorStoreComponent,
    get_embeddings_component,
    get_llm_component,
    get_node_store_component,
    get_vector_store_component,
)
from app.dependencies.services.chunks import Chunk


logger = structlog.stdlib.get_logger(__name__)


class Completion(BaseModel):
    response: str
    sources: list[Chunk] | None = None


class CompletionGen(BaseModel):
    response: TokenGen
    sources: list[Chunk] | None = None


class ChatService(metaclass=SingletonMetaClass):
    def __init__(
        self,
        llm_component: LLMComponent = get_llm_component(),
        vector_store_component: VectorStoreComponent = get_vector_store_component(),
        embedding_component: EmbeddingComponent = get_embeddings_component(),
        node_store_component: NodeStoreComponent = get_node_store_component(),
    ) -> None:
        self.llm_service = llm_component
        self.vector_store_component = vector_store_component
        self.storage_context = StorageContext.from_defaults(
            vector_store=vector_store_component.vector_store,
            docstore=node_store_component.doc_store,
            index_store=node_store_component.index_store,
        )
        self.service_context = ServiceContext.from_defaults(
            llm=llm_component.llm, embed_model=embedding_component.embedding_model
        )
        self.index = VectorStoreIndex.from_vector_store(
            vector_store=vector_store_component.vector_store,
            storage_context=self.storage_context,
            service_context=self.service_context,
            show_progress=True,
        )

    def _chat_engine(
        self, context_filter: ContextFilter | None = None
    ) -> BaseChatEngine:
        vector_index_retriever = self.vector_store_component.get_retriever(
            index=self.index, context_filter=context_filter
        )
        return ContextChatEngine.from_defaults(
            retriever=vector_index_retriever,
            service_context=self.service_context,
            node_postprocessors=[
                MetadataReplacementPostProcessor(target_metadata_key="window"),
            ],
        )

    def stream_chat(
        self,
        messages: list[ChatMessage],
        use_context: bool = False,
        context_filter: ContextFilter | None = None,
    ) -> CompletionGen:
        if use_context:
            last_message = messages[-1].content
            chat_engine = self._chat_engine(context_filter=context_filter)
            streaming_response = chat_engine.stream_chat(
                message=last_message if last_message is not None else "",
                chat_history=messages[:-1],
            )
            sources = [
                Chunk.from_node(node) for node in streaming_response.source_nodes
            ]
            completion_gen = CompletionGen(
                response=streaming_response.response_gen, sources=sources
            )
        else:
            stream = self.llm_service.llm.stream_chat(messages)
            completion_gen = CompletionGen(
                response=stream_chat_response_to_tokens(stream)
            )
        return completion_gen

    def chat(
        self,
        messages: list[ChatMessage],
        use_context: bool = False,
        context_filter: ContextFilter | None = None,
    ) -> Completion:
        if use_context:
            last_message = messages[-1].content
            chat_engine = self._chat_engine(context_filter=context_filter)
            wrapped_response = chat_engine.chat(
                message=last_message if last_message is not None else "",
                chat_history=messages[:-1],
            )
            sources = [Chunk.from_node(node) for node in wrapped_response.source_nodes]
            completion = Completion(response=wrapped_response.response, sources=sources)
        else:
            chat_response = self.llm_service.llm.chat(messages)
            response_content = chat_response.message.content
            response = response_content if response_content is not None else ""
            completion = Completion(response=response)
        return completion
