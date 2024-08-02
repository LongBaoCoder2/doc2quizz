from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_groq import ChatGroq

# Define prompt
prompt_template = """Write a concise summary of the following:
"{text}"
CONCISE SUMMARY:"""

FILE_PATH = "../data/Patch-level Routing in Mixture-of-Experts is Provably Sample-efficient for.pdf"
loader = PyPDFLoader(file_path=FILE_PATH)

prompt = PromptTemplate.from_template(prompt_template)
# Define LLM chain
llm = ChatGroq(temperature=0, model="llama3-8b-8192")
llm_chain = LLMChain(prompt=prompt, llm=llm)
# Define StuffDocumentsChain
stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="text")
docs = loader.load()
print(stuff_chain.run(docs))

llm_chain.get_prompts()