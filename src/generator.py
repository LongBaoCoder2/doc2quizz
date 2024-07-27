import logging
from typing import List, TypedDict, Literal
from pydantic import BaseModel, ValidationError, TypeAdapter
from pathlib import Path

from prompt import template_system_prompt, template_user_document, template_output
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI


log_filename = 'logs/debug.log'
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()  # Optionally log to the console as well
    ]
)

# Define the Pydantic Quiz class
class Quiz(BaseModel):
    question: str
    options: List[str]
    answer: str
    reasoning: str


class QuizGenerator:
    def __init__(self, api_key: str | None = None, model="gemini-pro", model_kwargs: dict = {}, text_splitter_kwargs: dict = {}):
        # Define the prompt template
        self.prompt_template = ChatPromptTemplate.from_messages([
                ("system", template_system_prompt),
                ("user", template_user_document)
        ])
        self.quiz_ta = TypeAdapter(List[Quiz])
        self.text_splitter = RecursiveCharacterTextSplitter(**text_splitter_kwargs)
        self.model = ChatGoogleGenerativeAI(api_key=api_key, 
                                            model="gemini-pro", 
                                            temperature=0,
                                            **model_kwargs)

        self.loader_classes = {
            'pdf': PyMuPDFLoader,
            # 'other_loader': OtherLoaderClass
        }


    # Function to load and split the PDF document
    def load_pdf(self, file_path: str, type_file: Literal["pdf"] = "pdf", **kwargs) -> List[Document]:
        logging.info(f"Loading PDF from path: {pdf_path}")

        document_loader = self.loader_classes[type_file](file_path=file_path)
        if document_loader is None:
            raise NotImplementedError(f"{self.loader_classes} is not supported yet.")

        # Load the PDF file as a list of Document objects
        documents = document_loader.load_and_split(self.text_splitter)
        logging.info(f"Loaded {len(documents)} document chunks from PDF")
        logging.debug(f"Type of {type(documents[0])}")

        return documents

    def parse_quizzes_from_response(self, response_content: str) -> List[Quiz]:
        """
        This function takes a string response from a LLM and 
        parses it into a list of Quiz objects.
        """

        # Find the start and end indices of the quiz data in the response
        # This is done by finding the first occurrence of '[' and the last occurrence of ']'
        left = response_content.find("[")
        right = response_content.rfind("]")

        # Extract the quiz data from the response using the found indices
        response_content = response_content[left: right + 1]

        try:
            # Attempt to validate the extracted quiz data as JSON
            # This will raise a ValidationError if the data is invalid
            list_quizzes = self.quiz_ta.validate_json(response_content)
        except ValidationError as e:
            # Log any validation errors that occur
            logging.error(f"Validation error: {e}")
            return []

        return list_quizzes

    def generate_quizzes_from_full_documents(self, documents: List[Document]) -> List[Quiz]:
        """
        This function generates quizzes from full documents by using a Large Language Model (LLM) to generate quiz questions.
        Args:
            documents (List[Document]): A list of Document objects containing the text to generate quizzes from.

        Returns:
            List[Quiz]: A list of Quiz objects containing the generated quizzes.
        """

        logging.info("Generating quizzes from documents")

        # Create a list of messages to send to the LLM model, where each message is a formatted prompt template
        messages = [self.prompt_template.format(document=document, number=2) for document in documents]

        # Send the messages to the LLM model in batches and retrieve the responses
        try:
            responses = self.model.batch(messages[:5])  # You can adjust the batch size as needed
        except Exception as e:
            logging.error(f"Error during LLM batch processing: {e}")
            return []

        # Iterate over the responses from the LLM model
        quizzes = []
        for response in responses:
            quizzes.extend(self.parse_quizzes_from_response(response.content))

        logging.info(f"Generated {len(quizzes)} quizzes")
        return quizzes


    def generate(self, pdf_path: str | Path) -> List[Quiz]:
        """
        This function generates quizzes from a PDF file by loading the PDF, splitting it into documents, and then generating quizzes from the documents.

        Args:
            pdf_path (str | Path): The path to the PDF file to generate quizzes from.

        Returns:
            List[Quiz]: A list of Quiz objects containing the generated quizzes.
        """

        # Load the PDF file and split it into documents
        documents = self.load_pdf(pdf_path)
        quizzes = self.generate_quizzes_from_full_documents(documents)
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

    
