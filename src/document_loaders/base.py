import logging
from typing import List
from abc import ABC, abstractmethod
from langchain_core.documents import Document


class DocumentLoader(ABC):
    @abstractmethod
    async def load(self, file_path: str) -> List[Document]:
        pass