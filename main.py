# main.py

import config
from orchestrator.orchestrator_agent import OrchestratorAgent
from ingestion.ingest_agent import DocumentIngestionAgent
from policy.rule_agent import PolicyRuleAgent
from retrieval.retrieval_agent import RetrievalAgent
from compliance.compliance_agent import ComplianceAgent
from rewrite.rewrite_agent import RewriteAgent
from reporting.report_agent import ReportAgent

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
    policy_path = "sample_policy.txt"
    policy_agent = PolicyRuleAgent(orchestrator.shared_state)
    rules = policy_agent.process_policy(policy_path)

    print("\n--- Shared State After Phase 2 ---")
    print(orchestrator.shared_state)
    print("----------------------------------\n")

    # Phase 3 — Retrieve relevant rules
    retrieval_agent = RetrievalAgent(orchestrator.shared_state)
    relevant_rules = retrieval_agent.find_relevant_rules()

    print("\n--- Relevant Rules Found (Phase 3) ---")
    print("--------------------------------------")
    if relevant_rules:
        for r in relevant_rules:
            print(f"[{r['rule_id']}] {r['text']}")
    else:
        print("No matching policy rules detected.")
    print("--------------------------------------\n")

    # Phase 4 — Compliance Evaluation
    compliance_agent = ComplianceAgent(orchestrator.shared_state)
    violations = compliance_agent.evaluate_compliance()

    print("\n--- Compliance Report (Phase 4) ---")
    if violations:
        for v in violations:
            print(f"❌ [{v['rule_id']}] {v['rule_text']}")
            print(f"   Evidence → \"{v['evidence']}\"")
            print(f"   Severity → {v['severity']}\n")
    else:
        print("✔ Document is fully compliant — no issues detected.")
    print("--------------------------------------\n")

    # Phase 5 — Rewrite suggestions  (FIXED INDENTATION)
    rewrite_agent = RewriteAgent(orchestrator.shared_state)
    rewrites = rewrite_agent.generate_rewrites()

    print("\n--- Rewrite Suggestions (Phase 5) ---")
    if rewrites:
        for r in rewrites:
            print(f"\nRule {r['rule_id']} Fix:")
            print(f"⚠ Original: {r['original_text']}")
            print(f"✅ Suggestion: {r['rewrite_suggestion']}")
    else:
        print("No rewrites needed — the document is compliant.")
    print("--------------------------------------\n")

    # Phase 6 — Final Report Generation
    report_agent = ReportAgent(orchestrator.shared_state)
    final_report = report_agent.generate_text_report()
    report_agent.save_report("final_report.txt")
    report_agent.export_json("final_report.json")

    print("\n=== Final Compliance Report (Phase 6) ===")
    print(final_report)
    print("Report saved as final_report.txt and final_report.json")
    print("===========================================\n")

    return orchestrator.shared_state


if __name__ == "__main__":
    run("sample_doc.txt")
