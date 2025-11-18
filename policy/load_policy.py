# policy/load_policy.py

import os

def read_policy(filepath):
    """Return raw text from a policy file."""
    ext = os.path.splitext(filepath)[1].lower()

    if ext == ".txt":
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()

    elif ext == ".pdf":
        try:
            import fitz
        except Exception:
            raise RuntimeError("PyMuPDF required for PDF extraction. pip install pymupdf")
        doc = fitz.open(filepath)
        return "\n".join([page.get_text() for page in doc])

    elif ext == ".docx":
        try:
            import docx
        except Exception:
            raise RuntimeError("python-docx required. pip install python-docx")
        doc = docx.Document(filepath)
        return "\n".join([p.text for p in doc.paragraphs])

    else:
        raise ValueError(f"Unsupported policy format: {ext}")
