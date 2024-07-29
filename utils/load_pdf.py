from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from utils.gpt_config import OPENAI_KEY

async def load_pdf(pdf_path: str, question: str) -> str:
    loader = PyPDFLoader(pdf_path)
    pages = loader.load_and_split()
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_KEY)
    faiss_index = FAISS.from_documents(pages, embeddings)
    docs = faiss_index.similarity_search(question, k=4)
    context = "\n\n".join([doc.page_content for doc in docs])

    return context 