python
import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

# ================================
# Configuration
# ================================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
INDEX_PATH = "faiss_index_storage"  # Folder where the index will be saved

if not OPENAI_API_KEY:
    raise ValueError("Please set your OPENAI_API_KEY environment variable")

# Initialize OpenAI embeddings
embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)

# ================================
# Document Loading
# ================================
def load_documents(file_path):
    """Reads a text file and returns a list of Document objects."""
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
# Vector Store Logic (Save/Load)
# ================================
def get_or_create_vector_store(file_path):
    """Loads a local FAISS index if it exists; otherwise, creates and saves a new one."""
    
    # 1. Try to load from disk
    if os.path.exists(INDEX_PATH):
        print("⚡ Loading existing vector store from disk...")
        # allow_dangerous_deserialization=True is required for pickle-based loading
        return FAISS.load_local(
            INDEX_PATH, 
            embeddings, 
            allow_dangerous_deserialization=True
        )
    
    # 2. If not found, create new one
    print("🚀 Creating new vector store (this will use OpenAI credits)...")
    docs = load_documents(file_path)
    if not docs:
        raise ValueError("No documents found to index.")
        
    vector_store = FAISS.from_documents(docs, embeddings)
    
    # 3. Save for future use
    vector_store.save_local(INDEX_PATH)
    print(f"💾 Vector store saved to '{INDEX_PATH}'")
    
    return vector_store

# ================================
# Example Usage
# ================================
if __name__ == "__main__":
    sample_file = "sample_faqs.txt" # Ensure this file exists
    
    try:
        faiss_store = get_or_create_vector_store(sample_file)
        
        # Simple test query
        query = "What is the return policy?"
        results = faiss_store.similarity_search(query, k=1)
        
        if results:
            print(f"\n🔍 Search Test:\nQuery: {query}\nResult: {results[0].page_content}")
            
    except Exception as e:
        print(f"❌ Error: {e}")