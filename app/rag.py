from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class RAGPipeline:
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
        self.model = AutoModelForCausalLM.from_pretrained("distilgpt2")

    def run(self, query):
        docs = self.vector_store.query(query, top_k=3)
        context = "\n".join([doc["text"] for doc in docs])
        full_prompt = f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"

        inputs = self.tokenizer(full_prompt, return_tensors="pt")
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=100,
            temperature=0.7,
            pad_token_id=self.tokenizer.eos_token_id
        )
        generated = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        answer = generated.split("Answer:")[-1].strip()

        return {
            "question": query,
            "answer": answer,
            "sources": list(set([doc["source"] for doc in docs]))
        }
