from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class RAGPipeline:
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
        self.model = AutoModelForCausalLM.from_pretrained("distilgpt2")

    def run(self, query):
        # Step 1: Retrieve top matching documents
        docs = self.vector_store.query(query, top_k=3)

        # Step 2: Create a single context string
        context = "\n\n".join([doc["text"] for doc in docs])
        full_prompt = (
            f"Context:\n{context}\n\n"
            f"Question: {query}\n"
            f"Answer:"
        )

        # Step 3: Generate an answer from the language model
        inputs = self.tokenizer(full_prompt, return_tensors="pt")
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=200,
            temperature=0.7,
            pad_token_id=self.tokenizer.eos_token_id
        )
        decoded = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Step 4: Extract only the answer
        answer = decoded.split("Answer:")[-1].strip()

        # Step 5: Create citations in the proper format
        citations = []
        for doc in docs:
            citation_text = doc["text"].strip()
            if len(citation_text) > 300:
                citation_text = citation_text[:300].strip() + "..."
            citations.append({
                "text": citation_text,
                "source": doc["source"]
            })

        return {
            "answer": answer,
            "citations": citations
        }
