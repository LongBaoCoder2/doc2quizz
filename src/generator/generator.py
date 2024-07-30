import logging
from typing import List, TypedDict, Literal
from pathlib import Path

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

from generator.prompt import template_system_prompt, template_user_document, template_output
from parser import Quiz, QuizParse


DEFAULT_MODEL_NAME = "gemini-pro"

class QuizGenerator:
    def __init__(self, api_key: str | None = None, 
                 model: str | None = "gemini-pro", 
                 model_kwargs: dict = {}, 
                 text_splitter_kwargs: dict = {}):
        self.model_kwargs = model_kwargs
        self.api_key = api_key

        self.text_splitter = RecursiveCharacterTextSplitter(**text_splitter_kwargs)
        self.parser = QuizParse()
        self.model_name = model if model is not None \
                                else DEFAULT_MODEL_NAME
        
        self.loader_classes = {
            'pdf': PyMuPDFLoader,
            # 'other_loader': OtherLoaderClass
        }

    # Function to load and split the PDF document
    async def load_pdf(self, file_path: str, type_file: Literal["pdf"] = "pdf", **kwargs) -> List[Document]:
        logging.info(f"Loading PDF from path: {file_path}")

        document_loader = self.loader_classes[type_file](file_path=file_path)
        if document_loader is None:
            raise NotImplementedError(f"{self.loader_classes} is not supported yet.")

        # Load the PDF file as a list of Document objects
        # documents = document_loader.load_and_split(self.text_splitter)
        doc_iter = await document_loader.aload()
        logging.info(f"Loaded {len(doc_iter)} document chunks from PDF")
        logging.debug(f"Type of {type(doc_iter[0])}")

        return doc_iter

    async def generate_from_full_documents(self, documents: List[Document]) -> List[Quiz]:
        """
        This function generates quizzes from full documents by using a Large Language Model (LLM) to generate quiz questions.
        Args:
            documents (List[Document]): A list of Document objects containing the text to generate quizzes from.

        Returns:
            List[Quiz]: A list of Quiz objects containing the generated quizzes.
        """

        logging.info("Generating quizzes from documents")

        # Create a list of messages to send to the LLM model, where each message is a formatted prompt template
        system_prompt = self.parser.format(template_system_prompt)
        self.prompt_template = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                ("user", template_user_document)
        ])

        messages = [self.prompt_template.format(document=document, number=2) for document in documents]
        self.model = ChatGoogleGenerativeAI(api_key=self.api_key, 
                                        model=self.model_name, 
                                        temperature=0,
                                        **self.model_kwargs)

        # Send the messages to the LLM model in batches and retrieve the responses
        try:
            responses = await self.model.abatch(messages[:5])  # You can adjust the batch size as needed
        except Exception as e:
            logging.error(f"Error during LLM batch processing: {e}")
            return []

        # Iterate over the responses from the LLM model
        quizzes = []
        for response in responses:
            quizzes.extend(self.parser.parse(response.content))

        logging.info(f"Generated {len(quizzes)} quizzes")
        return quizzes


    async def generate(self, pdf_path: str | Path) -> List[Quiz]:
        """
        This function generates quizzes from a PDF file by loading the PDF, splitting it into documents, and then generating quizzes from the documents.

        Args:
            pdf_path (str | Path): The path to the PDF file to generate quizzes from.

        Returns:
            List[Quiz]: A list of Quiz objects containing the generated quizzes.
        """

        # Load the PDF file and split it into documents
        logging.debug("Start generate: ")

        documents = await self.load_pdf(pdf_path)

        logging.debug("Start generate: ")

        quizzes = await self.generate_from_full_documents(documents)
        return quizzes


def merge_quizzes(quizzes: List[Quiz]) -> str:
    logging.info("Merging quizzes into a single response")

    merged_response = "\n\n".join([template_output.format(
                index=i, 
                question=quiz.question,
                option_a=quiz.options[0],
                option_b=quiz.options[1],
                option_c=quiz.options[2],
                option_d=quiz.options[3],
                answer=quiz.answer,
                reasoning=quiz.reasoning
            )  for i, quiz in enumerate(quizzes)
        ])
    return merged_response

# Example usage
if __name__ == "__main__":
    quiz_generator = QuizGenerator()

    pdf_path = 'data/Patch-level Routing in Mixture-of-Experts is Provably Sample-efficient for.pdf'

    quizzes = quiz_generator.generate(pdf_path)
    final_response = merge_quizzes(quizzes)
    
    logging.info("Final Merged Response:")
    print(final_response)

    
