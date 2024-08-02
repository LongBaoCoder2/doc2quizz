from .base import BaseLLM
from .gemini import GeminiLLM
from .groq import GroqLLM


all_base_model = {
    "groq": GroqLLM,
    "gemini": GeminiLLM
}

class NotSupportedLLMException(Exception):
    pass


def get_llm_model(base_model: str) -> BaseLLM:
    model = all_base_model[base_model]
    if model is None:
        raise NotSupportedLLMException("{} is not supported yet. Try {}").format(
                base_model, " ,".join(list(all_base_model)
        ))
    
    return model