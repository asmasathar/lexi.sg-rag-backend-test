import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from app.document_loader import sentence_chunker

class VectorStore:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")  
        self.texts = []
        self.meta = []
        self.index = faiss.IndexFlatL2(384)

    def add_documents(self, docs):
        for doc in docs:
            chunks = sentence_chunker(doc["text"], sentences_per_chunk=5) 
            embeddings = self.model.encode(chunks)
            self.index.add(np.array(embeddings).astype("float32"))
            self.texts.extend(chunks)
            self.meta.extend([{"source": doc["source"], "chunk_id": i} for i in range(len(chunks))])
    def query(self, question, top_k=3):
        q_embed = self.model.encode([question]).astype("float32")
        D, I = self.index.search(np.array(q_embed), top_k)
        results = []
        for i in I[0]:
            results.append({
                "text": self.texts[i],
                "source": self.meta[i]["source"]
            })
        return results
