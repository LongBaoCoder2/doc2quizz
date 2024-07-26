from typing import List
from prompt import template_prompt


from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

prompt_template = PromptTemplate.from_template(template_prompt)

def load_pdf(pdf_path: str):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)

    # Initialize the PyMuPDF loader
    loader = PyMuPDFLoader(file_path=pdf_path)
    # Load the PDF file as a list of Document objects
    documents = loader.load_and_split(text_splitter)

    return documents

def call_api_to_generate_quizz(documents: List[Document]):
    # db = Chroma.from_documents(documents[:15], 
    #                            GoogleGenerativeAIEmbeddings(model="models/embedding-001"),
    #                            persist_directory="./chroma_db")
    llm = ChatGoogleGenerativeAI(model="gemini-pro",
                                 temperature=0)
    response = llm.invoke(prompt_template.format(document=documents[1]))
    return response.content


# Example usage
if __name__ == "__main__":
    pdf_path = 'data/Patch-level Routing in Mixture-of-Experts is Provably Sample-efficient for.pdf'
    documents = load_pdf(pdf_path)
    print(len(documents))
    print(call_api_to_generate_quizz(documents))
