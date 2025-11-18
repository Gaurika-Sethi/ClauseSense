# orchestrator/orchestrator_agent.py

import uuid
import datetime
import os

class OrchestratorAgent:
    """
    Phase 0 Agent:
    - Validates input file
    - Initializes shared state memory
    - Generates metadata (document_id, timestamp, file_extension)
    - Prepares the pipeline for ingestion
    """

    SUPPORTED_FORMATS = ("pdf", "docx", "txt")

    def __init__(self):
        # Shared state accessible by all agents
        self.shared_state = {}

    def _get_extension(self, filepath):
        return os.path.basename(filepath).split(".")[-1].lower()

    def initialize_document(self, filepath):
        """
        Validates the file, extracts metadata, stores values into shared_state.
        Returns a metadata dictionary.
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")

        ext = self._get_extension(filepath)
        if ext not in self.SUPPORTED_FORMATS:
            raise ValueError(
                f"Unsupported file type: {ext}. Supported formats are: {self.SUPPORTED_FORMATS}"
            )

        # Generate a short unique ID
        document_id = "DOC_" + str(uuid.uuid4())[:8]
        timestamp = datetime.datetime.utcnow().isoformat() + "Z"

        metadata = {
            "document_id": document_id,
            "file_path": filepath,
            "file_extension": ext,
            "timestamp": timestamp,
            "status": "INITIALIZED",
        }

        # Save to shared memory so next agents can use it
        self.shared_state["document_metadata"] = metadata

        print("\n[PHASE 0] Document Initialization Complete")
        print("----------------------------------------")
        print(f" Document ID   : {document_id}")
        print(f" File Path     : {filepath}")
        print(f" File Extension: {ext}")
        print(f" Timestamp     : {timestamp}")
        print("----------------------------------------\n")

        return metadata