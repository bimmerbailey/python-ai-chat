from functools import lru_cache

from llama_index.vector_stores.milvus import DEFAULT_DOC_ID_KEY, DEFAULT_EMBEDDING_KEY
from pydantic import AnyHttpUrl, MongoDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class MongoSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="mongo_")
    # hostname: str = "mongo"
    hostname: str = "localhost"
    port: int = 27017
    password: str = "password"
    name: str = "rag_app"
    username: str = "rag_user"

    url: MongoDsn = f"mongodb://{hostname}:{port}/{name}"


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
    model_config = SettingsConfigDict(env_prefix="redis_")

    # dsn: RedisDsn = "redis://redis:6379"
    host: str = "localhost"
    port: int = 6379
    dsn: RedisDsn = f"redis://{host}:{port}"


class MilvusSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="milvus_")

    # uri: AnyHttpUrl = "http://milvus-db"
    uri: AnyHttpUrl = f"http://localhost"
    hostname: str = str(uri).split("/")[-1]
    collection_name: str = "ragCollection"
    token: str = ""
    dim: int = 384
    embedding_field: str = DEFAULT_EMBEDDING_KEY
    doc_id_field: str = DEFAULT_DOC_ID_KEY
    similarity_metric: str = "IP"
    consistency_level: str = "Strong"
    overwrite: bool = False
    text_key: str | None = None


class S3Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="s3_")

    # uri: AnyHttpUrl = "http://minio:9000"
    uri: AnyHttpUrl = "http://localhost:9000"
    bucket: str = "a-bucket"
    aws_access_key_id: str = "minioadmin"
    aws_secret_access_key: str = "minioadmin"


mongo_settings = MongoSettings()
jwt_settings = JwtSettings()
app_settings = AppSettings()
redis_settings = RedisSettings()
milvus_settings = MilvusSettings()
s3_settings = S3Settings()


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
