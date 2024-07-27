import logging
from typing import List
from pydantic import BaseModel, ValidationError, TypeAdapter

from prompt import template_system_prompt, template_user_document, template_output
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI


log_filename = 'logs/debug.log'
logging.basicConfig(
    level=logging.INFO,
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

quiz_ta = TypeAdapter(List[Quiz])

# Define the prompt template
prompt_template = ChatPromptTemplate.from_messages([
    ("system", template_system_prompt),
    ("user", template_user_document)
])

# Function to load and split the PDF document
def load_pdf(pdf_path: str) -> List[Document]:
    logging.info(f"Loading PDF from path: {pdf_path}")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)

    # Initialize the PyMuPDF loader
    loader = PyMuPDFLoader(file_path=pdf_path)
    # Load the PDF file as a list of Document objects
    documents = loader.load_and_split(text_splitter)
    logging.info(f"Loaded {len(documents)} document chunks from PDF")

    return documents

# Function to parse the LLM response into Quiz objects
def parse_quizzes_from_response(response_content: str) -> List[Quiz]:
    quizzes = []
    # Assume each response contains quiz questions separated by new lines
    left = response_content.find("[")
    right = response_content.rfind("]")

    response_content = response_content[left: right + 1]

    try:
        list_quizzes = quiz_ta.validate_json(response_content)
    except ValidationError as e:
        logging.error(f"Validation error: {e}")

    return list_quizzes

# Function to generate quizzes from full documents
def generate_quizzes_from_full_documents(documents: List[Document]) -> List[Quiz]:
    logging.info("Generating quizzes from documents")

    llm = ChatGoogleGenerativeAI(model="gemini-pro", 
                                 temperature=0)
    messages = [prompt_template.format(document=document, number=2) for document in documents]
    try:
        responses = llm.batch(messages[:5])  # You can adjust the batch size as needed
    except Exception as e:
        logging.error(f"Error during LLM batch processing: {e}")
        return []
    # Parse each response into Quiz objects
    quizzes = []

    for response in responses:
        logging.info(f"Parse response: \n{response.content}")
        quizzes.extend(parse_quizzes_from_response(response.content))
        logging.info("Parse successfully: \n")
    
    logging.info(f"Generated {len(quizzes)} quizzes")
    return quizzes

# Function to merge all quizzes into a single response
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
    pdf_path = 'data/Patch-level Routing in Mixture-of-Experts is Provably Sample-efficient for.pdf'
    documents = load_pdf(pdf_path)

    logging.info("Start generating quizzes:")
    quizzes = generate_quizzes_from_full_documents(documents)
    final_response = merge_quizzes(quizzes)
    
    logging.info("Final Merged Response:")
    print(final_response)
