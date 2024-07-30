from pydantic import BaseModel

class BaseConfig(BaseModel):
    api_key: str | None = None
    model: str = "gemini-pro"
    model_kwargs: dict = {}
    text_splitter_kwargs: dict = {}
