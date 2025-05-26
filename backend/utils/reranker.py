def rerank(query, documents, top_k=5):
    query_words = set(query.lower().split())
    scored = []
    for doc in documents:
        doc_words = set(doc['text'].lower().split())
        score = len(query_words & doc_words)
        scored.append((score, doc))
    scored.sort(reverse=True)
    return [doc for score, doc in scored[:top_k]]
