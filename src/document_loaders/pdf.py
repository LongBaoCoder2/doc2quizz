import logging
from typing import List

from langchain_core.documents import Document
from langchain_community.document_loaders import PyMuPDFLoader

from .base import DocumentLoader

class PDFLoader(DocumentLoader):
    def __init__(self, text_splitter):
        self.text_splitter = text_splitter

    async def aload(self, file_path: str) -> List[Document]:
        loader = PyMuPDFLoader(file_path=file_path)
        doc_iter = await loader.aload()
        return self.text_splitter.split_documents(doc_iter)