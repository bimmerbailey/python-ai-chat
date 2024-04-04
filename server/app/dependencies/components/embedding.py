from functools import lru_cache

from llama_index.core.embeddings import BaseEmbedding, MockEmbedding
from llama_index.embeddings.huggingface import (  # type: ignore
    HuggingFaceEmbedding,
)

from app.config.settings import AppSettings, get_app_settings
from app.paths import models_cache_path


class EmbeddingComponent:
    embedding_model: BaseEmbedding

    def __init__(self, app_settings: AppSettings = get_app_settings()) -> None:
        if app_settings.fastapi_env != "testing":
            self.embedding_model = HuggingFaceEmbedding(
                model_name=app_settings.embedding_hf_model_name,
                cache_folder=str(models_cache_path),
            )
        else:
            self.embedding_model = MockEmbedding(384)


@lru_cache
def get_embeddings_component() -> EmbeddingComponent:
    return EmbeddingComponent()
