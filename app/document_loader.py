import os
import docx
import PyPDF2

def load_documents(data_dir="data"):
    docs = []
    for fname in os.listdir(data_dir):
        path = os.path.join(data_dir, fname)
        text = ""

        # Handle DOCX files
        if fname.endswith(".docx"):
            print(f"📄 Reading DOCX: {fname}")
            try:
                doc = docx.Document(path)
                text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
            except Exception as e:
                print(f"❌ Error reading DOCX {fname}: {e}")
                continue

        # Handle PDF files
        elif fname.endswith(".pdf"):
            print(f"📕 Reading PDF: {fname}")
            try:
                with open(path, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    text = "\n".join([
                        page.extract_text()
                        for page in reader.pages
                        if page.extract_text()
                    ])
            except Exception as e:
                print(f"❌ Error reading PDF {fname}: {e}")
                continue

        # Add document if text was successfully extracted
        if text:
            docs.append({
                "filename": fname,
                "text": text
            })

    print(f"\n✅ Loaded {len(docs)} documents successfully.")
    return docs
