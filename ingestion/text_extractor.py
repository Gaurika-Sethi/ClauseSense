# ingestion/text_extractor.py

import os

def extract_text_from_txt(filepath):
    """Extract text from a simple TXT file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def extract_text_from_pdf(filepath):
    """
    Optional PDF extraction.
    Requires: pip install pymupdf
    """
    try:
        import fitz  # PyMuPDF
    except Exception:
        raise RuntimeError("PyMuPDF is required. Install with: pip install pymupdf")

    doc = fitz.open(filepath)
    text_blocks = []

    for page in doc:
        text_blocks.append(page.get_text())

    return "\n".join(text_blocks)


def extract_text_from_docx(filepath):
    """
    Optional DOCX extraction.
    Requires: pip install python-docx
    """
    try:
        import docx
    except Exception:
        raise RuntimeError("python-docx required. Install: pip install python-docx")

    doc = docx.Document(filepath)
    paras = [p.text for p in doc.paragraphs]
    return "\n".join(paras)


def split_into_sections(raw_text):
    """
    Basic heuristic splitting.
    Splits text into paragraphs separated by blank lines.
    """
    sections = [s.strip() for s in raw_text.split("\n\n") if s.strip()]

    # Fallback: large documents with no newlines
    if not sections:
        sections = [raw_text[i:i+400] for i in range(0, len(raw_text), 400)]

    return sections