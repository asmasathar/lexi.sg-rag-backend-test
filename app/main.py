from fastapi import FastAPI
from pydantic import BaseModel
from app.document_loader import load_documents
from app.vector_store import VectorStore
from app.rag import RAGPipeline
from fastapi.responses import RedirectResponse

class Query(BaseModel):
    query: str

app = FastAPI()

@app.get("/")
def redirect_to_docs():
    return RedirectResponse("/docs")

documents = load_documents("data")
store = VectorStore()
store.add_documents(documents)
rag_pipeline = RAGPipeline(store)

@app.post("/query")
def query_rag(q: Query):
    result = rag_pipeline.run(q.query)
    return result
