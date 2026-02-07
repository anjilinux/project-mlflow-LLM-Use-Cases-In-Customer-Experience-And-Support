# vector_store.py
import os
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document

# Load OpenAI API key from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Please set your OPENAI_API_KEY environment variable")

# Initialize embeddings
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

def load_documents(file_path: str):
    """
    Reads a text file and returns a list of LangChain Document objects.
    Each line is treated as a separate document.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"{file_path} not found")
    documents = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                documents.append(Document(page_content=line))
    return documents

def create_vector_store(documents):
    """
    Creates a FAISS vector store from a list of Document objects.
    """
    return FAISS.from_documents(documents, embeddings)

if __name__ == "__main__":
    # Jenkins-friendly: use env variable or default
    sample_file = os.getenv("SAMPLE_FAQ_FILE", "sample_faqs.txt")
    try:
        docs = load_documents(sample_file)
        faiss_store = create_vector_store(docs)
        print(f"✅ Vector store created with {len(docs)} documents")
    except Exception as e:
        print(f"❌ Error creating vector store: {e}")
        exit(1)
