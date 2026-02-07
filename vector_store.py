# vector_store.py

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document
import os

# ================================
# Load OpenAI API Key
# ================================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Please set your OPENAI_API_KEY environment variable")

# Initialize OpenAI embeddings
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

# ================================
# Load Documents
# ================================
def load_documents(file_path):
    """
    Reads a text file and returns a list of LangChain Document objects.
    Each line is treated as a separate document.
    """
    documents = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                documents.append(Document(page_content=line))
    return documents

# ================================
# Create FAISS Vector Store
# ================================
def create_vector_store(documents):
    """
    Creates a FAISS vector store from a list of Document objects.
    """
    vector_store = FAISS.from_documents(documents, embeddings)
    return vector_store

# ================================
# Example Usage
# ================================
if __name__ == "__main__":
    sample_file = "sample_faqs.txt"  # Make sure this file exists
    docs = load_documents(sample_file)
    faiss_store = create_vector_store(docs)
    print(f"✅ Vector store created with {len(docs)} documents")
