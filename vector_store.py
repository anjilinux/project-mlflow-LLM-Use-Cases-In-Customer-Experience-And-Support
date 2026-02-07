import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

# ================================
# Configuration
# ================================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "dummy")  # fallback to "dummy" if not set
INDEX_PATH = "faiss_index_storage"  # folder to save FAISS index

# Initialize OpenAI embeddings
embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)

# ================================
# Document Loading
# ================================
def load_documents(file_path):
    """Read a text file and return a list of Document objects (one line per document)."""
    if not os.path.exists(file_path):
        print(f"⚠️ Warning: File '{file_path}' not found.")
        return []

    documents = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                documents.append(Document(page_content=line))
    return documents

# ================================
# Vector Store Logic
# ================================
def get_or_create_vector_store(file_path):
    """Load FAISS index from disk or create a new one if not exists."""
    if os.path.exists(INDEX_PATH):
        print("⚡ Loading existing FAISS vector store from disk...")
        return FAISS.load_local(
            INDEX_PATH,
            embeddings,
            allow_dangerous_deserialization=True  # required for recent versions
        )

    print("🚀 Creating new FAISS vector store (this may use OpenAI credits)...")
    docs = load_documents(file_path)
    if not docs:
        raise ValueError("No documents found to index.")

    vector_store = FAISS.from_documents(docs, embeddings)
    vector_store.save_local(INDEX_PATH)
    print(f"💾 Vector store saved to '{INDEX_PATH}'")
    return vector_store

# ================================
# Example Usage
# ================================
if __name__ == "__main__":
    sample_file = "sample_faqs.txt"  # Make sure this file exists
    try:
        faiss_store = get_or_create_vector_store(sample_file)

        # Simple test query
        query = "What is the return policy?"
        results = faiss_store.similarity_search(query, k=1)

        if results:
            print(f"\n🔍 Query: {query}\nResult: {results[0].page_content}")
        else:
            print("⚠️ No results found.")

    except Exception as e:
        print(f"❌ Error: {e}")
