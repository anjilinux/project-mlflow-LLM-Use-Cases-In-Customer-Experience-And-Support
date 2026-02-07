# vector_store.py
import os
from pathlib import Path
from loguru import logger

# Try modern LangChain OpenAI embeddings import
try:
    from langchain_openai import OpenAIEmbeddings
except ModuleNotFoundError:
    try:
        from langchain.embeddings.openai import OpenAIEmbeddings
    except ModuleNotFoundError:
        raise ImportError(
            "Cannot import OpenAIEmbeddings. Make sure 'langchain-openai' is installed."
        )

from langchain.vectorstores import FAISS
from langchain.docstore.document import Document

# Load OpenAI API key from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Please set your OPENAI_API_KEY environment variable")

# Initialize embeddings
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)


def load_documents(file_path: str) -> list[Document]:
    """
    Reads a text file and returns a list of LangChain Document objects.
    Each line is treated as a separate document.
    """
    if not Path(file_path).exists():
        raise FileNotFoundError(f"{file_path} does not exist")
    
    documents = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                documents.append(Document(page_content=line))
    logger.info(f"Loaded {len(documents)} documents from {file_path}")
    return documents


def create_vector_store(documents: list[Document], persist_path: str | None = None) -> FAISS:
    """
    Creates a FAISS vector store from a list of Document objects.
    If persist_path is provided, the store will be saved to disk.
    """
    vector_store = FAISS.from_documents(documents, embeddings)
    
    if persist_path:
        persist_dir = Path(persist_path)
        persist_dir.mkdir(parents=True, exist_ok=True)
        vector_store.save_local(str(persist_dir))
        logger.info(f"Vector store saved to {persist_dir.resolve()}")
    
    return vector_store


def load_vector_store(persist_path: str) -> FAISS:
    """
    Loads a FAISS vector store from disk.
    """
    persist_dir = Path(persist_path)
    if not persist_dir.exists():
        raise FileNotFoundError(f"Vector store path {persist_path} does not exist")
    
    vector_store = FAISS.load_local(str(persist_dir), embeddings)
    logger.info(f"Vector store loaded from {persist_dir.resolve()}")
    return vector_store


if __name__ == "__main__":
    # Example usage
    sample_file = "sample_faqs.txt"  # Make sure this file exists
    persist_dir = "vector_store"

    try:
        docs = load_documents(sample_file)
        faiss_store = create_vector_store(docs, persist_path=persist_dir)
        logger.success(f"Vector store created with {len(docs)} documents")
    except Exception as e:
        logger.error(f"Failed to create vector store: {e}")
