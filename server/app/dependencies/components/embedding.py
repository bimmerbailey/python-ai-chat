from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from llama_index import MockEmbedding
from llama_index.embeddings.base import BaseEmbedding

from app.config.settings import AppSettings, get_app_settings
from app.dependencies.base import SingletonMetaClass
from app.paths import models_cache_path


class EmbeddingComponent(metaclass=SingletonMetaClass):
    embedding_model: BaseEmbedding

    def __init__(
        self,
        app_settings: Annotated[
            AppSettings, Depends(get_app_settings)
        ] = get_app_settings(),
    ) -> None:
        if app_settings.fastapi_env != "testing":
            from llama_index.embeddings import HuggingFaceEmbedding

            self.embedding_model = HuggingFaceEmbedding(
                model_name=app_settings.embedding_hf_model_name,
                cache_folder=str(models_cache_path),
            )
        else:
            self.embedding_model = MockEmbedding(384)


@lru_cache
def get_embeddings_component() -> EmbeddingComponent:
    return EmbeddingComponent()
