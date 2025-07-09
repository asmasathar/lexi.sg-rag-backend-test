import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class VectorStore:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")  
        self.texts = []
        self.meta = []
        self.index = faiss.IndexFlatL2(384)

    def add_documents(self, docs):
        for doc in docs:
            chunks = [doc["text"][i:i+500] for i in range(0, len(doc["text"]),500)]
            embeddings = self.model.encode(chunks)
            self.index.add(np.array(embeddings).astype("float32"))
            self.texts.extend(chunks)
            self.meta.extend([{"source": doc["filename"], "chunk_id": i} for i in range(len(chunks))])

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
