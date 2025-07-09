import os
import re
from docx import Document
from PyPDF2 import PdfReader


def clean_text(text):
    """Clean up special characters and excess whitespace."""
    text = re.sub(r'\s+', ' ', text)
    text = text.replace('\u00a0', ' ')
    return text.strip()


def simple_sentence_tokenize(text):
    """A basic sentence splitter using regex (without nltk)."""
    # Split on '.', '?', '!' followed by space or end of string
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]


def sentence_chunker(text, sentences_per_chunk=3):
    """Split text into chunks of full sentences."""
    sentences = simple_sentence_tokenize(text)
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
    """Extract raw text from a PDF file."""
    try:
        reader = PdfReader(file_path)
        return "\n".join([page.extract_text() or "" for page in reader.pages])
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return ""


def extract_text_from_docx(file_path):
    """Extract raw text from a DOCX file."""
    try:
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return ""


def load_documents(directory):
    """Load, clean, chunk, and return documents from a folder."""
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
