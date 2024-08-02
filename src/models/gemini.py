from typing import Optional, List

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages.base import BaseMessage

from .base import BaseLLM


default_gemini_model = "gemini-pro"

valid_gemini_models = ['gemini-pro',
                       'models/chat-bison-001',
                       'models/text-bison-001',
                       'models/embedding-gecko-001',
                       'models/gemini-1.0-pro-latest',
                       'models/gemini-1.0-pro',
                       'models/gemini-pro',
                       'models/gemini-1.0-pro-001',
                       'models/gemini-1.0-pro-vision-latest',
                       'models/gemini-pro-vision',
                       'models/gemini-1.5-pro-latest',
                       'models/gemini-1.5-pro-001',
                       'models/gemini-1.5-pro',
                       'models/gemini-1.5-flash-latest',
                       'models/gemini-1.5-flash-001',
                       'models/gemini-1.5-flash',
                       'models/embedding-001',
                       'models/text-embedding-004',
                       'models/aqa']



class GeminiLLM(BaseLLM):
    def __init__(self, config, model: Optional[str] = None):        
        self.config = config
        if isinstance(model, str):
            model_name = model
            if model_name not in valid_gemini_models:
                raise ValueError(
                    f"Invalid model. Available GPT models: {', '.join(model for model in valid_gpt_models)}"
                )
        elif model is None:
            model_name = default_gemini_model

        super().__init__(model_name)
        self.model = self.load_model()


    def load_model(self, *args, **kwargs):
        return ChatGoogleGenerativeAI(
            api_key=self.config.api_key,
            model=self.model_name,
            temperature=0,
            **self.config.model_kwargs
        )

    def generate(self, prompt: str, *args, **kwargs) -> str:
        response = self.model.invoke(prompt, *args, **kwargs)
        return response.content

    async def a_generate(self, prompt: str, *args, **kwargs) -> str:
        response = await self.model.ainvoke(prompt, *args, **kwargs)
        return response.content

    async def a_batch(self, messages: List[str], *args, **kwargs) -> List[BaseMessage]:
        responses = await self.model.abatch(messages, *args, **kwargs)
        return responses

    def get_model_name(self, *args, **kwargs) -> str:
        return self.model_name