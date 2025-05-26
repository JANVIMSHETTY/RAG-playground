from typing import List

def chunk_text(text: str, max_length: int = 500, overlap: int = 50) -> List[str]:
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = min(start + max_length, len(words))
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += max_length - overlap

    return chunks
