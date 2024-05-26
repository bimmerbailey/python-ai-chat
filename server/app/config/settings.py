from functools import lru_cache
from typing import Literal
import os

from pydantic import AnyHttpUrl, BaseModel, Field, MongoDsn, RedisDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class MongoSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="mongo_")
    hostname: str = "mongo"
    port: int = 27017
    password: SecretStr = "password"
    name: str = "rag_app"
    username: str = "rag_user"

    @property
    def database_url(self) -> MongoDsn:
        if not os.environ.get("MONGO_URL", None):
            return MongoDsn(f"mongodb://{self.hostname}:{self.port}/{self.name}")
        return MongoDsn(os.environ.get("MONGO_URL"))


class JwtSettings(BaseSettings):
    model_config = SettingsConfigDict(frozen=True, env_prefix="jwt_")
    secret_key: str = "secret"
    algorithm: str = "HS256"
    token_expires: int = 60


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(frozen=True)

    url_base: str = "localhost"
    log_level: str = "DEBUG"
    json_logs: bool = False
    fastapi_env: str = "production"
    cookie_name: str = "cookie"

    llm_hf_repo_id: str = "TheBloke/Mistral-7B-Instruct-v0.1-GGUF"
    llm_hf_model_file: str = "mistral-7b-instruct-v0.1.Q4_K_M.gguf"
    embedding_hf_model_name: str = "BAAI/bge-small-en-v1.5"


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="REDIS_")

    host: str = "redis"
    port: int = 6379
    dsn: RedisDsn = f"redis://{host}:{port}"


class MilvusSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="MILVUS_")

    uri: AnyHttpUrl = "http://milvus-db"
    hostname: str = str(uri).split("/")[-1]
    collection_name: str = "ragCollection"
    token: str = ""
    dim: int = 768
    # embedding_field: str = DEFAULT_EMBEDDING_KEY
    # doc_id_field: str = DEFAULT_DOC_ID_KEY
    similarity_metric: str = "IP"
    consistency_level: str = "Strong"
    overwrite: bool = False
    text_key: str | None = None


class S3Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="S3_")

    uri: AnyHttpUrl = "http://minio:9000"
    bucket: str = "a-bucket"
    aws_access_key_id: str = "minioadmin"
    aws_secret_access_key: str = "minioadmin"


class EmbeddingSettings(BaseSettings):
    mode: Literal["huggingface", "openai", "sagemaker", "mock", "ollama"] = "ollama"
    ingest_mode: Literal["simple", "batch", "parallel"] = Field(
        "simple",
        description=(
            "The ingest mode to use for the embedding engine:\n"
            "If `simple` - ingest files sequentially and one by one. It is the historic behaviour.\n"
            "If `batch` - if multiple files, parse all the files in parallel, "
            "and send them in batch to the embedding model.\n"
            "If `parallel` - parse the files in parallel using multiple cores, and embedd them in parallel.\n"
            "`parallel` is the fastest mode for local setup, as it parallelize IO RW in the index.\n"
            "For modes that leverage parallelization, you can specify the number of "
            "workers to use with `count_workers`.\n"
        ),
    )
    count_workers: int = Field(
        2,
        description=(
            "The number of workers to use for file ingestion.\n"
            "In `batch` mode, this is the number of workers used to parse the files.\n"
            "In `parallel` mode, this is the number of workers used to parse the files and embed them.\n"
            "This is only used if `ingest_mode` is not `simple`.\n"
            "Do not go too high with this number, as it might cause memory issues. (especially in `parallel` mode)\n"
            "Do not set it higher than your number of threads of your CPU."
        ),
    )


class LLMSettings(BaseModel):
    mode: Literal[
        "llamacpp", "openai", "openailike", "azopenai", "sagemaker", "mock", "ollama"
    ] = "ollama"
    max_new_tokens: int = Field(
        256,
        description="The maximum number of token that the LLM is authorized to generate in one completion.",
    )
    context_window: int = Field(
        3900,
        description="The maximum number of context tokens for the model.",
    )
    tokenizer: str = Field(
        None,
        description="The model id of a predefined tokenizer hosted inside a model repo on "
        "huggingface.co. Valid model ids can be located at the root-level, like "
        "`bert-base-uncased`, or namespaced under a user or organization name, "
        "like `HuggingFaceH4/zephyr-7b-beta`. If not set, will load a tokenizer matching "
        "gpt-3.5-turbo LLM.",
    )
    temperature: float = Field(
        0.1,
        description="The temperature of the model. Increasing the temperature will make the model answer more creatively. A value of 0.1 would be more factual.",
    )


class LlamaCPPSettings(BaseModel):
    llm_hf_repo_id: str | None = None  # Come back to this, it wasn't optional
    llm_hf_model_file: str | None = None  # Come back to this, it wasn't optional
    prompt_style: Literal["default", "llama2", "tag", "mistral", "chatml"] = Field(
        "mistral",
        description=(
            "The prompt style to use for the chat engine. "
            "If `default` - use the default prompt style from the llama_index. It should look like `role: message`.\n"
            "If `llama2` - use the llama2 prompt style from the llama_index. Based on `<s>`, `[INST]` and `<<SYS>>`.\n"
            "If `tag` - use the `tag` prompt style. It should look like `<|role|>: message`. \n"
            "If `mistral` - use the `mistral prompt style. It shoudl look like <s>[INST] {System Prompt} [/INST]</s>[INST] { UserInstructions } [/INST]"
            "`llama2` is the historic behaviour. `default` might work better with your custom models."
        ),
    )

    tfs_z: float = Field(
        1.0,
        description="Tail free sampling is used to reduce the impact of less probable tokens from the output. A higher value (e.g., 2.0) will reduce the impact more, while a value of 1.0 disables this setting.",
    )
    top_k: int = Field(
        40,
        description="Reduces the probability of generating nonsense. A higher value (e.g. 100) will give more diverse answers, while a lower value (e.g. 10) will be more conservative. (Default: 40)",
    )
    top_p: float = Field(
        0.9,
        description="Works together with top-k. A higher value (e.g., 0.95) will lead to more diverse text, while a lower value (e.g., 0.5) will generate more focused and conservative text. (Default: 0.9)",
    )
    repeat_penalty: float = Field(
        1.1,
        description="Sets how strongly to penalize repetitions. A higher value (e.g., 1.5) will penalize repetitions more strongly, while a lower value (e.g., 0.9) will be more lenient. (Default: 1.1)",
    )


class RerankSettings(BaseSettings):
    enabled: bool = Field(
        False,
        description="This value controls whether a reranker should be included in the RAG pipeline.",
    )
    model: str = Field(
        "cross-encoder/ms-marco-MiniLM-L-2-v2",
        description="Rerank model to use. Limited to SentenceTransformer cross-encoder models.",
    )
    top_n: int = Field(
        2,
        description="This value controls the number of documents returned by the RAG pipeline.",
    )


class RagSettings(BaseModel):
    similarity_top_k: int = Field(
        2,
        description="This value controls the number of documents returned by the RAG pipeline or considered for reranking if enabled.",
    )
    similarity_value: float = Field(
        None,
        description="If set, any documents retrieved from the RAG must meet a certain match score. Acceptable values are between 0 and 1.",
    )
    rerank: RerankSettings = RerankSettings()  # Come back to this, it wasn't optional


class OllamaSettings(BaseModel):
    api_base: str = Field(
        "http://192.168.0.235:11434",
        description="Base URL of Ollama API. Example: 'https://localhost:11434'.",
    )
    embedding_api_base: str = Field(
        "http://192.168.0.235:11434",
        description="Base URL of Ollama embedding API. Example: 'https://localhost:11434'.",
    )
    llm_model: str = Field(
        "llama3",
        description="Model to use. Example: 'llama2-uncensored'.",
    )
    embedding_model: str = Field(
        'nomic-embed-text',
        description="Model to use. Example: 'nomic-embed-text'.",
    )
    keep_alive: str = Field(
        "5m",
        description="Time the model will stay loaded in memory after a request. examples: 5m, 5h, '-1' ",
    )
    tfs_z: float = Field(
        1.0,
        description="Tail free sampling is used to reduce the impact of less probable tokens from the output. A higher value (e.g., 2.0) will reduce the impact more, while a value of 1.0 disables this setting.",
    )
    num_predict: int = Field(
        None,
        description="Maximum number of tokens to predict when generating text. (Default: 128, -1 = infinite generation, -2 = fill context)",
    )
    top_k: int = Field(
        40,
        description="Reduces the probability of generating nonsense. A higher value (e.g. 100) will give more diverse answers, while a lower value (e.g. 10) will be more conservative. (Default: 40)",
    )
    top_p: float = Field(
        0.9,
        description="Works together with top-k. A higher value (e.g., 0.95) will lead to more diverse text, while a lower value (e.g., 0.5) will generate more focused and conservative text. (Default: 0.9)",
    )
    repeat_last_n: int = Field(
        64,
        description="Sets how far back for the model to look back to prevent repetition. (Default: 64, 0 = disabled, -1 = num_ctx)",
    )
    repeat_penalty: float = Field(
        1.1,
        description="Sets how strongly to penalize repetitions. A higher value (e.g., 1.5) will penalize repetitions more strongly, while a lower value (e.g., 0.9) will be more lenient. (Default: 1.1)",
    )
    request_timeout: float = Field(
        120.0,
        description="Time elapsed until ollama times out the request. Default is 120s. Format is float. ",
    )


def get_jwt_settings() -> JwtSettings:
    return JwtSettings()


def get_mongo_settings() -> MongoSettings:
    return MongoSettings()


@lru_cache
def get_app_settings() -> AppSettings:
    return AppSettings()


@lru_cache
def get_milvus_settings() -> MilvusSettings:
    return MilvusSettings()


@lru_cache
def get_s3_settings() -> S3Settings:
    return S3Settings()


@lru_cache
def get_redis_settings() -> RedisSettings:
    return RedisSettings()


@lru_cache
def get_embeddings_settings() -> EmbeddingSettings:
    return EmbeddingSettings()


def get_llm_settings() -> LLMSettings:
    return LLMSettings()


def get_llamacpp_settings() -> LlamaCPPSettings:
    return LlamaCPPSettings()


def get_rag_settings() -> RagSettings:
    return RagSettings()


def get_ollama_settings() -> OllamaSettings:
    return OllamaSettings()
