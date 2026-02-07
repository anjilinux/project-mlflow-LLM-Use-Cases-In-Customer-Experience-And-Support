from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from config import Config

def load_vector_store(texts):
    """
    Build and return FAISS vector store
    """
    embeddings = OpenAIEmbeddings(
        model=Config.EMBEDDING_MODEL  # e.g., "text-embedding-3-small"
    )

    vector_store = FAISS.from_texts(texts, embeddings)
    return vector_store
