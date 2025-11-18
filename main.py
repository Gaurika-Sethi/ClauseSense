# main.py

from orchestrator.orchestrator_agent import OrchestratorAgent
from ingestion.ingest_agent import DocumentIngestionAgent
from policy.rule_agent import PolicyRuleAgent

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
    
    # Phase 2
    policy_path = "sample_policy.txt"  # Place a small dummy file
    policy_agent = PolicyRuleAgent(orchestrator.shared_state)
    rules = policy_agent.process_policy(policy_path)

    print("\n--- Shared State After Phase 2 ---")
    print(orchestrator.shared_state)
    print("----------------------------------\n")

    return extracted


if __name__ == "__main__":
    run("sample_doc.txt")   # Make sure this file exists!