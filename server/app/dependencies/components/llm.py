from functools import lru_cache
from typing import Annotated, Callable, Any, Dict, List, Optional, Tuple, Union

import structlog
from fastapi import Depends
from llama_index.core.llms.llm import LLM
from llama_index.core.llms.mock import MockLLM
from llama_index.core.settings import Settings as LlamaIndexSettings
from llama_index.core.utils import set_global_tokenizer
from llama_index.llms.llama_cpp import LlamaCPP
from transformers import AutoTokenizer  # type: ignore

from app.config.settings import (
    AppSettings,
    LlamaCPPSettings,
    LLMSettings,
    get_app_settings,
    get_llamacpp_settings,
    get_llm_settings,
    OllamaSettings,
    get_ollama_settings,
)
from app.dependencies.components.prompt_helper import get_prompt_style
from app.paths import models_cache_path, models_path

logger = structlog.stdlib.get_logger(__name__)


class LLMComponent:
    llm: LLM

    def __init__(
        self,
        app_settings: AppSettings = get_app_settings(),
        llm_settings: LLMSettings = get_llm_settings(),
        ollama_settings: OllamaSettings = get_ollama_settings(),
        llamacpp_settings: LlamaCPPSettings = get_llamacpp_settings(),
    ) -> None:
        match llm_settings.mode:
            case "llamacpp":
                if llm_settings.tokenizer:
                    set_global_tokenizer(
                        AutoTokenizer.from_pretrained(
                            pretrained_model_name_or_path=llm_settings.tokenizer,
                            cache_dir=str(models_cache_path),
                        )
                    )
                prompt_style = get_prompt_style(llamacpp_settings.prompt_style)
                settings_kwargs = {
                    "tfs_z": llamacpp_settings.tfs_z,  # ollama and llama-cpp
                    "top_k": llamacpp_settings.top_k,  # ollama and llama-cpp
                    "top_p": llamacpp_settings.top_p,  # ollama and llama-cpp
                    "repeat_penalty": llamacpp_settings.repeat_penalty,  # ollama llama-cpp
                    "n_gpu_layers": -1,
                    "offload_kqv": True,
                }
                self.llm = LlamaCPP(
                    model_path=str(models_path / app_settings.llm_hf_model_file),
                    temperature=llm_settings.temperature,
                    max_new_tokens=llm_settings.max_new_tokens,
                    context_window=llm_settings.context_window,
                    generate_kwargs={},
                    callback_manager=LlamaIndexSettings.callback_manager,
                    # All to GPU
                    model_kwargs=settings_kwargs,
                    # transform inputs into Llama2 format
                    messages_to_prompt=prompt_style.messages_to_prompt,
                    completion_to_prompt=prompt_style.completion_to_prompt,
                    verbose=True,
                )
            case "ollama":
                try:
                    from llama_index.llms.ollama import Ollama  # type: ignore
                except ImportError as e:
                    raise ImportError(
                        "Ollama dependencies not found, install with `poetry install --extras llms-ollama`"
                    ) from e

                settings_kwargs = {
                    "tfs_z": ollama_settings.tfs_z,  # ollama and llama-cpp
                    "num_predict": ollama_settings.num_predict,  # ollama only
                    "top_k": ollama_settings.top_k,  # ollama and llama-cpp
                    "top_p": ollama_settings.top_p,  # ollama and llama-cpp
                    "repeat_last_n": ollama_settings.repeat_last_n,  # ollama
                    "repeat_penalty": ollama_settings.repeat_penalty,  # ollama llama-cpp
                }

                self.llm = Ollama(
                    model=ollama_settings.llm_model,
                    base_url=ollama_settings.api_base,
                    temperature=llm_settings.temperature,
                    context_window=llm_settings.context_window,
                    additional_kwargs=settings_kwargs,
                    request_timeout=ollama_settings.request_timeout,
                )

                if (
                    ollama_settings.keep_alive
                    != ollama_settings.model_fields["keep_alive"].default
                ):
                    # Modify Ollama methods to use the "keep_alive" field.
                    def add_keep_alive(func: Callable[..., Any]) -> Callable[..., Any]:
                        def wrapper(*args: Any, **kwargs: Any) -> Any:
                            kwargs["keep_alive"] = ollama_settings.keep_alive
                            return func(*args, **kwargs)

                        return wrapper

                    Ollama.chat = add_keep_alive(Ollama.chat)
                    Ollama.stream_chat = add_keep_alive(Ollama.stream_chat)
                    Ollama.complete = add_keep_alive(Ollama.complete)
                    Ollama.stream_complete = add_keep_alive(Ollama.stream_complete)
            case "mock":
                self.llm = MockLLM()


@lru_cache
def get_llm_component() -> LLMComponent:
    return LLMComponent()
