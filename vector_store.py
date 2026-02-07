from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from config import Config

def load_vector_store(texts):
    embeddings = OpenAIEmbeddings(model=Config.EMBEDDING_MODEL)
    return FAISS.from_texts(texts, embeddings)
