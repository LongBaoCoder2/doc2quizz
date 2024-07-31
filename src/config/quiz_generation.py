from pydantic import BaseModel

class QuizGeneratorConfig(BaseModel):
    api_key: str = None
    model: str = "gemini-pro"
    model_kwargs: dict = {}
    text_splitter_kwargs: dict = {}