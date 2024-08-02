from typing import Optional, List
from langchain_core.messages.base import BaseMessage
from langchain_groq import ChatGroq

from .base import BaseLLM

default_groq_model = "mixtral-8x7b-32768"

class GroqLLM(BaseLLM):
    def __init__(self, config, model_name: Optional[str] = None):
        self.config = config
        self.model_name = model_name or default_groq_model
        self.model = self.load_model()
        super().__init__(model_name)

    def load_model(self, *args, **kwargs):
        return ChatGroq(
            groq_api_key=self.config.api_key,
            model_name=self.model_name,
            temperature=0,
            **self.config.model_kwargs
        )

    def generate(self, prompt: str, *args, **kwargs) -> str:
        response = self.model.invoke(prompt, *args, **kwargs)
        return response.content

    async def a_generate(self, prompt: str, *args, **kwargs) -> str:
        response = await self.model.ainvoke(prompt, *args, **kwargs)
        return response.content

    async def a_batch(self, prompts: List[str], *args, **kwargs) -> List[BaseMessage]:
        responses = await self.model.abatch(prompts, *args, **kwargs)
        return responses

    def get_model_name(self, *args, **kwargs) -> str:
        return self.model_name

    def batch_generate(self, prompts: List[str], *args, **kwargs) -> List[str]:
        # Implementing this method for GroqLLM, unlike GeminiLLM
        responses = self.model.batch(prompts, *args, **kwargs)
        return [response.content for response in responses]