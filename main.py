# main.py

import config
import json
from orchestrator.orchestrator_agent import OrchestratorAgent
from ingestion.ingest_agent import DocumentIngestionAgent
from policy.rule_agent import PolicyRuleAgent
from retrieval.retrieval_agent import RetrievalAgent
from compliance.compliance_agent import ComplianceAgent
from rewrite.rewrite_agent import RewriteAgent
from reporting.report_agent import ReportAgent
from config import GEMINI_API_KEY, GEMINI_MODEL

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
    if not violations:
        print("✔ Document is fully compliant — no issues detected.")
    else:
        for v in violations:
            status = "❌" if not v.get("is_compliant", True) else "✔"
            rule = v.get("rule_id", "Unknown")
            explanation = v.get("explanation", "No explanation provided.")
            evidence = v.get("evidence", "(no evidence provided)")

            print(f"{status} [{rule}] {explanation}")
            print(f"   Evidence → \"{evidence}\"\n")

    # Phase 4.5 — Explanations + Confidence
    from rule_explaination import generate_rule_explanations
    explanations = generate_rule_explanations(
        orchestrator.shared_state["sections"],
        relevant_rules
    )

    orchestrator.shared_state["explanations"] = explanations

    # ★ NEW: Extract confidence and store in proper structure
    confidence_scores = {}
    for rule_id, items in explanations.items():
        confidence_scores[rule_id] = [
            {
                "section": entry["section"],
                "confidence": entry.get("confidence", 0.0)
            }
            for entry in items
        ]

    orchestrator.shared_state["confidence_scores"] = confidence_scores

    # Debug output
    print("\n--- Rule Explanations with Confidence Scores ---")
    for rule_id, items in explanations.items():
        print(f"\n### {rule_id} ###")
        for entry in items:
            print(f"- Section: {entry['section']}")
            print(f"  Confidence: {entry['confidence']}")
            print(f"  Explanation: {entry['explanation']}")
    print("----------------------------------\n")



    # Phase 5 — Rewrite Suggestions
    orchestrator.shared_state["config"] = {
        "GEMINI_API_KEY": GEMINI_API_KEY,
        "MODEL": GEMINI_MODEL
    }

    rewrite_agent = RewriteAgent(orchestrator.shared_state)
    rewrites = rewrite_agent.generate_rewrites()

    print("\n--- Rewrite Suggestions (Phase 5) ---")
    if not rewrites:
        print("No rewrites needed.")
    else:
        for r in rewrites:
            print(f"\n🔁 Rule {r['rule_id']} Fix:")
            print(f"• Issue: {r['rule_text']}")
            print(f"• Original: {r['original']}")
            print(f"• Suggested Rewrite: {r['rewrite']}")
    print("--------------------------------------")

    print("CONFIDENCE DEBUG =", orchestrator.shared_state.get("confidence_scores"))

    # Phase 7.4 — Unify
    from reconstruction.unifier import unify_results
    orchestrator.shared_state["unified"] = unify_results(orchestrator.shared_state)

    print("\n--- Unified Results (Phase 7.4) ---")
    for u in orchestrator.shared_state["unified"]:
        print(json.dumps(u, indent=4))

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
