from vector_store import load_vector_store

def retrieve_context(query, docs):
    vector_db = load_vector_store(docs)
    results = vector_db.similarity_search(query, k=2)
    return "\n".join([r.page_content for r in results])
