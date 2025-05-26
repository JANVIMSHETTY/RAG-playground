from utils.embedding import model
from vector_db.qdrant_client import search_documents

def self_query_rag_pipeline(query: str, top_k: int = 5):
    query_embedding = model.encode([query])[0]
    search_results = search_documents("your_collection_name", query_embedding, top_k)
    chunks = [res.payload["chunk"] for res in search_results]
    # Dummy self-query logic
    answer = f"It talks about: {chunks[0][:100]}..." if chunks else "No content found."
    return {"answer": answer.strip(), "retrieved_chunks": chunks}
