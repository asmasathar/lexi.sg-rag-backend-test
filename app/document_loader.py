import os
import re
import nltk
from nltk.tokenize import sent_tokenize
from docx import Document
from PyPDF2 import PdfReader

# Use /tmp for nltk data to ensure it’s writable in Render
NLTK_DATA_DIR = "/tmp/nltk_data"
os.makedirs(NLTK_DATA_DIR, exist_ok=True)
nltk.data.path.append(NLTK_DATA_DIR)

# Download 'punkt' safely into /tmp
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt", download_dir=NLTK_DATA_DIR)

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = text.replace('\u00a0', ' ')
    return text.strip()

def sentence_chunker(text, sentences_per_chunk=3):
    sentences = sent_tokenize(text)
    chunks = []
    current_chunk = ""
    for i, sentence in enumerate(sentences):
        current_chunk += sentence + " "
        if (i + 1) % sentences_per_chunk == 0:
            chunks.append(current_chunk.strip())
            current_chunk = ""
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def extract_text_from_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        return "\n".join([page.extract_text() or "" for page in reader.pages])
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return ""

def extract_text_from_docx(file_path):
    try:
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return ""

def load_documents(directory):
    documents = []
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if filename.endswith(".pdf"):
            raw_text = extract_text_from_pdf(filepath)
        elif filename.endswith(".docx"):
            raw_text = extract_text_from_docx(filepath)
        else:
            continue

        cleaned = clean_text(raw_text)
        chunks = sentence_chunker(cleaned, sentences_per_chunk=3)

        for chunk in chunks:
            documents.append({
                "text": chunk,
                "source": filename
            })

    return documents
