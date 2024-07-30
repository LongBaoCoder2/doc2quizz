import logging
import os

from .base import BaseModel, BaseLLM



class GPTModel(BaseLLM):
    def __init__(
        self,
        model: str | None = None,
        _openai_api_key: str | None = None,
        *args,
        **kwargs,
    ):
        model_name = None
        if isinstance(model, str):
            model_name = model
            if model_name not in valid_gpt_models:
                raise ValueError(
                    f"Invalid model. Available GPT models: {', '.join(model for model in valid_gpt_models)}"
                )
        elif model is None:
            model_name = default_gpt_model

        self._openai_api_key = _openai_api_key
        # args and kwargs will be passed to the underlying model, in load_model function
        self.args = args
        self.kwargs = kwargs
        super().__init__(model_name)