import requests
import os

HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")  # from Railway env vars

def query_hf_model(prompt: str):
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": prompt,
        "parameters": {
            "temperature": 0.7,
            "max_new_tokens": 300
        }
    }

    response = requests.post(
        "https://api-inference.huggingface.co/models/tiiuae/falcon-rw-1b",
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        return response.json()[0]["generated_text"]
    else:
        print("🚨 Hugging Face API Error:", response.text)
        return "Sorry, something went wrong with the model."
