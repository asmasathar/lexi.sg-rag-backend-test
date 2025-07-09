from app.vector_store import VectorStore
from app.model import generate_answer

class RAGPipeline:
    def __init__(self, store: VectorStore):
        self.store = store

    def run(self, query: str, top_k: int = 3):
        retrieved_chunks = self.store.query(query, top_k=top_k)
        
        context = "\n".join([chunk["text"] for chunk in retrieved_chunks])
        
        answer = generate_answer(context, query)
        
        return {
            "answer": answer,
            "citations": retrieved_chunks
        }
