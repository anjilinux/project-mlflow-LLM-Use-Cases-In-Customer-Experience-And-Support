# vector_store.py
from langchain.embeddings.openai import OpenAIEmbeddings  # correct
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document
import os

# Load your OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Please set your OPENAI_API_KEY environment variable")

# Initialize embeddings
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

def load_documents(file_path):
    documents = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                documents.append(Document(page_content=line))
    return documents

def create_vector_store(documents):
    return FAISS.from_documents(documents, embeddings)

if __name__ == "__main__":
    sample_file = "sample_faqs.txt"
    docs = load_documents(sample_file)
    faiss_store = create_vector_store(docs)
    print(f"Vector store created with {len(docs)} documents")
