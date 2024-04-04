from functools import lru_cache
from typing import Annotated

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
        llamacpp_settings: LlamaCPPSettings = get_llamacpp_settings(),
    ) -> None:
        llm_mode = llm_settings.mode
        if llm_settings.tokenizer:
            set_global_tokenizer(
                AutoTokenizer.from_pretrained(
                    pretrained_model_name_or_path=llm_settings.tokenizer,
                    cache_dir=str(models_cache_path),
                )
            )

        logger.info("Initializing the LLM in mode=%s", llm_mode)
        if app_settings.fastapi_env != "testing":
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
        else:
            self.llm = MockLLM()


@lru_cache
def get_llm_component() -> LLMComponent:
    return LLMComponent()
