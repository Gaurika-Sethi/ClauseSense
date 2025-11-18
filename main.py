# main.py

from orchestrator.orchestrator_agent import OrchestratorAgent
from ingestion.ingest_agent import DocumentIngestionAgent


def run(filepath):
    # Phase 0
    orchestrator = OrchestratorAgent()
    metadata = orchestrator.initialize_document(filepath)

    # Phase 1
    ingestion_agent = DocumentIngestionAgent(orchestrator.shared_state)
    extracted = ingestion_agent.ingest(metadata, filepath)

    print("\n--- Shared State After Phase 1 ---")
    print(orchestrator.shared_state)
    print("----------------------------------\n")

    return extracted


if __name__ == "__main__":
    run("sample_doc.txt")   # Make sure this file exists!