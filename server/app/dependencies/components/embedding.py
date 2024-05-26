from functools import lru_cache

from llama_index.core.embeddings import BaseEmbedding, MockEmbedding

from app.config.settings import (
    AppSettings,
    get_app_settings,
    OllamaSettings,
    get_ollama_settings,
    EmbeddingSettings,
    get_embeddings_settings,
)
from app.paths import models_cache_path


class EmbeddingComponent:
    embedding_model: BaseEmbedding

    def __init__(
        self,
        app_settings: AppSettings = get_app_settings(),
        ollama_settings: OllamaSettings = get_ollama_settings(),
        embeddings_settings: EmbeddingSettings = get_embeddings_settings(),
    ) -> None:
        match embeddings_settings.mode:
            case "huggingface":
                try:
                    from llama_index.embeddings.huggingface import HuggingFaceEmbedding  # type: ignore
                except ImportError as e:
                    raise ImportError(
                        "Local dependencies not found, install with "
                        "`poetry install --extras embeddings-huggingface`"
                    ) from e
                self.embedding_model = HuggingFaceEmbedding(
                    model_name=app_settings.embedding_hf_model_name,
                    cache_folder=str(models_cache_path),
                )
            case "ollama":
                try:
                    from llama_index.embeddings.ollama import (  # type: ignore
                        OllamaEmbedding,
                    )
                except ImportError as e:
                    raise ImportError(
                        "Local dependencies not found, install with `poetry install --extras embeddings-ollama`"
                    ) from e

                self.embedding_model = OllamaEmbedding(
                    model_name=ollama_settings.embedding_model,
                    base_url=ollama_settings.embedding_api_base,
                )
            case "mock":
                self.embedding_model = MockEmbedding(384)


@lru_cache
def get_embeddings_component() -> EmbeddingComponent:
    return EmbeddingComponent()
