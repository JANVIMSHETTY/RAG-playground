from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from uuid import uuid4

client = QdrantClient(host="localhost", port=6333)

def init_qdrant_collection(collection_name: str, vector_size: int):
    if collection_name not in [col.name for col in client.get_collections().collections]:
        client.recreate_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )

def insert_documents(collection_name: str, chunks: list, embeddings: list):
    points = [
        PointStruct(
            id=str(uuid4()),
            vector=embedding,
            payload={"chunk": chunk},
        )
        for chunk, embedding in zip(chunks, embeddings)
    ]
    client.upsert(collection_name=collection_name, points=points)

def search_documents(collection_name: str, query_embedding: list, top_k: int):
    results = client.search(
        collection_name=collection_name,
        query_vector=query_embedding,
        limit=top_k,
        with_payload=True
    )
    return results
