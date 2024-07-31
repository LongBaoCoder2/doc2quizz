import logging
from typing import List, Literal
from pathlib import Path

from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI

from src.generator.prompt import template_system_prompt, template_user_document, template_output
from src.parser import Quiz, QuizParse
from src.config.quiz_generation import QuizGeneratorConfig
from src.document_loaders.pdf import PDFLoader


DEFAULT_MODEL_NAME = "gemini-pro"

class QuizGenerator:
    def __init__(self, config: QuizGeneratorConfig):
        self.config = config
        self.text_splitter = RecursiveCharacterTextSplitter(**config.text_splitter_kwargs)
        self.parser = QuizParse()
        self.model_name = config.model or DEFAULT_MODEL_NAME
        
        self.document_loaders = {
            'pdf': PDFLoader(self.text_splitter),
            # 'other_loader': OtherLoaderClass
        }
        self.model = ChatGoogleGenerativeAI(api_key=config.api_key,
                                            model=self.model_name,
                                            temperature=0,
                                            **config.model_kwargs)

    async def load_document(self, file_path: str, file_type: Literal["pdf"] = "pdf") -> List[Document]:
        logging.info(f"Loading document from path: {file_path}")

        loader = self.document_loaders.get(file_type)
        if loader is None:
            raise NotImplementedError(f"{file_type} is not supported yet.")
        
        documents = await loader.load(file_path)
        logging.info(f"Loaded {len(documents)} document chunks")
        return documents

    async def generate_from_documents(self, documents: List[Document]) -> List[Quiz]:
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
        documents = await self.load_document(pdf_path)

        logging.debug("Start generate: ")
        quizzes = await self.generate_from_documents(documents)

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

    
