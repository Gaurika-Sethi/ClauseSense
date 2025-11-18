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
        rewrites = self.shared_state.get("rewrites", [])

        lines = []
        lines.append("=== ClauseSense Compliance Report ===\n")
        lines.append(f"Generated On: {datetime.utcnow().isoformat()} UTC\n")

        # Metadata
        lines.append("\n--- Document Metadata ---")
        for k, v in metadata.items():
            lines.append(f"{k}: {v}")

        # Matched Rules
        lines.append("\n--- Matched Policy Rules ---")
        if matched_rules:
            for r in matched_rules:
                lines.append(f"[{r['rule_id']}] {r['text']}")
        else:
            lines.append("No matched rules.")

        # Violations
        lines.append("\n--- Violations Detected ---")
        if violations:
            for v in violations:
                lines.append(f"\n❌ {v['rule_id']} - {v['rule_text']}")
                lines.append(f"Evidence: {v['evidence']}")
                lines.append(f"Severity: {v['severity']}")
        else:
            lines.append("✔ No violations — fully compliant.")

        # Rewrite Suggestions
        lines.append("\n--- Rewrite Suggestions ---")
        if rewrites:
            for r in rewrites:
                lines.append(f"\nRule {r['rule_id']} Fix:")
                lines.append(f"Original: {r['original_text']}")
                lines.append(f"Suggestion: {r['rewrite_suggestion']}")
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
            "rewrites": self.shared_state.get("rewrites", []),
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(export_data, f, indent=4)
        return filename