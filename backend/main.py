from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional

from utils.pdf_utils import extract_text_from_pdf
from utils.chunking import chunk_text
from utils.embedding import embed_chunks
from vector_db.qdrant_client import init_qdrant_collection, insert_documents

from rag.basic_rag import basic_rag_pipeline
from rag.reranker_rag import reranker_rag_pipeline
from rag.self_query_rag import self_query_rag_pipeline

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    init_qdrant_collection(collection_name="your_collection_name", vector_size=384)

class QueryRequest(BaseModel):
    query: str
    rag_types: List[str]
    top_k: Optional[int] = 5

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    contents = await file.read()
    text = extract_text_from_pdf(contents)
    chunks = chunk_text(text)
    embeddings = embed_chunks(chunks)
    insert_documents("your_collection_name", chunks, embeddings)
    return {"message": "PDF uploaded and processed successfully", "chunks": len(chunks)}

@app.post("/query")
async def query_rag(request: QueryRequest):
    try:
        results = {}

        if "simple" in request.rag_types:
            results["simple"] = basic_rag_pipeline(request.query, request.top_k)

        if "reranker" in request.rag_types:
            results["reranker"] = reranker_rag_pipeline(request.query, request.top_k)

        if "self_query" in request.rag_types:
            results["self_query"] = self_query_rag_pipeline(request.query, request.top_k)

        return {"query": request.query, "results": results}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
