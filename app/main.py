import os
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager
import nltk
nltk.data.path.append("/tmp/nltk_data")
from app.document_loader import load_documents
from app.vector_store import VectorStore
from app.rag import RAGPipeline

class Query(BaseModel):
    query: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    data_path = "data"
    if not os.path.exists(data_path):
        print(f" WARNING: Data folder '{data_path}' not found.")
        yield 
        return

    try:
        documents = load_documents(data_path)
        vector_store = VectorStore()
        vector_store.add_documents(documents)
        rag_pipeline = RAGPipeline(vector_store)
        app.state.rag_pipeline = rag_pipeline
        print(" RAG pipeline initialized.")
    except Exception as e:
        print(f" Error initializing RAG pipeline: {e}")
    
    yield  

    

app = FastAPI(lifespan=lifespan)

@app.get("/")
def redirect_to_docs():
    return RedirectResponse("/docs")

@app.post("/query")
def query_rag(q: Query):
    rag_pipeline = getattr(app.state, "rag_pipeline", None)
    if rag_pipeline is None:
        return {"error": "RAG pipeline not initialized"}
    return rag_pipeline.run(q.query)
