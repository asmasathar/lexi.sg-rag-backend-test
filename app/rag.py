from openai import OpenAI
import re

class RAGPipeline:
    def __init__(self, vectorstore):
        self.vectorstore = vectorstore
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key="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"  
        )

    def format_prompt(self, context, query):
        return f"""
You are a legal assistant. Use only the following legal documents to answer the question. Do not use outside knowledge. Be concise, accurate, and cite the source below each point if relevant.

Context:
{context}

Question: {query}

Answer:"""

    def clean_answer(self, text):
        return re.sub(r'(\b.+?\b)(?: \1\b)+', r'\1', text).strip()

    def run(self, query):
        top_docs = self.vectorstore.query(query)
        context = "\n---\n".join([doc["text"] for doc in top_docs])
        prompt = self.format_prompt(context, query)

        response = self.client.chat.completions.create(
            model="tngtech/deepseek-r1t2-chimera:free",
            messages=[
                {"role": "system", "content": "You are a legal document QA assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=1024,
            extra_headers={
                "HTTP-Referer": "https://ragbackend.com",  # optional
                "X-Title": "Legal RAG System"  # optional
            }
        )

        answer = response.choices[0].message.content.strip()

        return {
            "answer": self.clean_answer(answer),
            "citations": [
                {
                    "text": doc["text"],
                    "source": doc["source"]
                } for doc in top_docs
            ]
        }
