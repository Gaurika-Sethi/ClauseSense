# main.py

from orchestrator.orchestrator_agent import OrchestratorAgent

def run_phase0(filepath):
    orchestrator = OrchestratorAgent()
    metadata = orchestrator.initialize_document(filepath)
    return metadata

if __name__ == "__main__":
    # Use your own sample file here
    # Example: "sample_doc.txt"
    run_phase0("sample_doc.txt")