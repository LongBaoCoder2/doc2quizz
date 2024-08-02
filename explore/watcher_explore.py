import os
import asyncio
from langchain_groq import ChatGroq
from langchain_community.embeddings import JinaEmbeddings
from langchain_community.vectorstores import FAISS
from src.generator.watcher import AgentWatcher
from src.document_loaders.pdf import PDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

async def main():
    # Initialize LLM, embeddings, and vector store
    llm = ChatGroq(temperature=0)
    embeddings = JinaEmbeddings(jina_api_key="jina_f2d64cca94d74d10b1e7c2a53b74e750HlCB7f2g4o0SxEiEeD_CLw95OkGv")
    
    # Load and process the document
    pdf_path = 'data/Patch-level Routing in Mixture-of-Experts is Provably Sample-efficient for.pdf'
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    loader = PDFLoader(text_splitter)
    documents = await loader.aload(pdf_path)
    
    # Create a vector store from the documents
    texts = [doc.page_content for doc in documents]
    metadatas = [doc.metadata for doc in documents]
    vector_store = FAISS.from_texts(texts, embeddings, metadatas=metadatas)
    
    # Initialize AgentWatcher
    agent_watcher = AgentWatcher(llm, embeddings, vector_store)
    
    # Example user prompt and topic
    user_prompt = "Generate quizzes about the sample efficiency of patch-level routing in Mixture-of-Experts models"
    topic = "sample efficiency in machine learning"
    
    # Process the request using AgentWatcher
    result = await agent_watcher.process_request(user_prompt, texts, topic)
    
    # Print the results
    print("AgentWatcher Results:")
    print("Relevant Documents:", result.get("documents"))
    print("Web Search Results:", result.get("web_search"))
    print("Vector DB Search Results:", result.get("vector_db_search"))
    print("Synthetic Data:", result.get("synthetic_data"))

if __name__ == "__main__":
    asyncio.run(main())