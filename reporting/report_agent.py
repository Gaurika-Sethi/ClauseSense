# reporting/report_agent.py

import json
from datetime import datetime

class ReportAgent:
    def __init__(self, shared_state):
        self.shared_state = shared_state

    def generate_text_report(self):
        metadata = self.shared_state.get("document_metadata", {})
        matched_rules = self.shared_state.get("matched_rules", [])
        violations = self.shared_state.get("violations", [])
        rewrite_suggestions = self.shared_state.get("rewrite_suggestions", [])
        explanations = self.shared_state.get("explanations", {})

        lines = []
        lines.append("=== ClauseSense Compliance Report ===\n")
        lines.append(f"Generated On: {datetime.utcnow().isoformat()} UTC\n")

        # Metadata
        lines.append("\n--- Document Metadata ---")
        for k, v in metadata.items():
            lines.append(f"{k}: {v}")

        # Matched Rules
        lines.append("\n\n--- Matched Policy Rules ---")
        if matched_rules:
            for r in matched_rules:
                lines.append(f"[{r['rule_id']}] {r['text']}")
        else:
            lines.append("No matched rules.")

        # Violations
        lines.append("\n\n--- Violations Detected ---")
        if violations:
            for v in violations:
                lines.append(f"\n❌ {v['rule_id']} - {v['rule_text']}")
                lines.append(f"Evidence: {v['evidence']}")
                lines.append(f"Severity: {v['severity']}")
        else:
            lines.append("✔ No violations — fully compliant.")

        # Explanations + Confidence Scores
        lines.append("\n\n--- Rule Explanations ---")
        if explanations:
            for rule_id, items in explanations.items():
                lines.append(f"\n### Rule {rule_id} ###")
                for entry in items:
                    lines.append(f"- Section: {entry['section']}")
                    lines.append(f"  Confidence: {entry.get('confidence', 'N/A')}")
                    lines.append(f"  Explanation: {entry['explanation']}")
        else:
            lines.append("No explanations available.")

        # Rewrite Suggestions
        lines.append("\n\n--- Rewrite Suggestions ---")
        if rewrite_suggestions:
            for r in rewrite_suggestions:
                lines.append(f"\n🔁 Rule {r['rule_id']} Fix:")
                lines.append(f"• Issue: {r['rule_text']}")
                lines.append(f"• Original: {r['original']}")
                lines.append(f"• Suggested Rewrite: {r['rewrite']}")
        else:
            lines.append("No rewrites needed.")

        report_text = "\n".join(lines)
        self.shared_state["final_report_text"] = report_text
        return report_text

    def save_report(self, filename="compliance_report.txt"):
        report_text = self.shared_state.get("final_report_text", "")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(report_text)
        return filename

    def export_json(self, filename="compliance_report.json"):
        export_data = {
            "metadata": self.shared_state.get("document_metadata", {}),
            "matched_rules": self.shared_state.get("matched_rules", []),
            "violations": self.shared_state.get("violations", []),
            "rewrite_suggestions": self.shared_state.get("rewrite_suggestions", []),
            "explanations": self.shared_state.get("explanations", {}),  # ✅ NEW
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(export_data, f, indent=4)
        return filename
