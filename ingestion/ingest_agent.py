# ingestion/ingest_agent.py

from .text_extractor import (
    extract_text_from_txt,
    extract_text_from_pdf,
    extract_text_from_docx,
    split_into_sections,
)


class DocumentIngestionAgent:
    """Phase 1 agent: extract raw text + split into sections."""

    def __init__(self, shared_state):
        self.shared_state = shared_state

    def ingest(self, metadata, filepath):
        ext = metadata.get("file_extension")

        print(f"[PHASE 1] Ingestion started for {filepath}")

        # Choose extraction method
        if ext == "txt":
            raw_text = extract_text_from_txt(filepath)
        elif ext == "pdf":
            raw_text = extract_text_from_pdf(filepath)
        elif ext == "docx":
            raw_text = extract_text_from_docx(filepath)
        else:
            raise ValueError(f"Unsupported file extension: {ext}")

        # Split into sections
        sections = split_into_sections(raw_text)

        # Save into shared_state
        self.shared_state["extracted_text"] = raw_text
        self.shared_state["sections"] = sections

        print(f"[PHASE 1] Extraction complete.")
        print(f" Total text length: {len(raw_text)} chars")
        print(f" Sections created : {len(sections)}\n")

        return {
            "status": "INGESTED",
            "text": raw_text,
            "sections": sections,
        }