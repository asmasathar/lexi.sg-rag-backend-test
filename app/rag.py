from app.vector_store import VectorStore
from app.model import generate_answer

class RAGPipeline:
    def __init__(self, store: VectorStore):
        self.store = store

    def run(self, query: str, top_k: int = 3):
        # 1. Retrieve top-k similar chunks from the vector DB
        retrieved_chunks = self.store.query(query, top_k=top_k)
        
        # 2. Prepare context by joining the retrieved texts
        context = "\n".join([chunk["text"] for chunk in retrieved_chunks])
        
        # 3. Generate answer using context + question
        answer = generate_answer(context, query)
        
        # 4. Return answer and citations (source + snippet)
        return {
            "answer": answer,
            "citations": retrieved_chunks
        }
