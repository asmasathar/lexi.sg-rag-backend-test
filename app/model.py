from transformers import pipeline

qa_pipeline = pipeline("text-generation", model="tiiuae/falcon-rw-1b")

def generate_answer(context, question):
    prompt = f"Context: {context}\n\nQuestion: {question}\n\nAnswer:"
    output = qa_pipeline(prompt, max_new_tokens=100)
    return output[0]["generated_text"].split("Answer:")[-1].strip()
