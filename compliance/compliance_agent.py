# compliance/compliance_agent.py

import json
from gemini.gemini_client import generate_completion, is_configured
from gemini.prompts.compliance_prompts import build_compliance_prompt
from gemini.utils import parse_json_safe              # <-- IMPORTANT

class ComplianceAgent:
    def __init__(self, shared_state):
        self.shared_state = shared_state

    def evaluate_compliance(self):
        violations = []

        matched_rules = self.shared_state.get("matched_rules", [])
        sections = self.shared_state.get("sections", [])

        for rule in matched_rules:
            for sec in sections:

                try:
                    prompt = build_compliance_prompt(rule["text"], sec)
                    raw_output = generate_completion(prompt)

                    result = parse_json_safe(raw_output)

                    # Ensure dict format
                    if not isinstance(result, dict):
                        raise ValueError("Gemini returned non-JSON")

                    # 🔐 Mandatory fields guaranteed
                    result.setdefault("rule_id", rule["rule_id"])
                    result.setdefault("rule_text", rule["text"])
                    result.setdefault("section", sec)
                    result.setdefault("status", "Violation")
                    result.setdefault("severity", "High")
                    result.setdefault("evidence", "(missing)")
                    result.setdefault("explanation", "(not provided)")

                except Exception:
                    # Fallback object
                    result = {
                        "rule_id": rule["rule_id"],
                        "rule_text": rule["text"],
                        "section": sec,
                        "status": "Violation",
                        "severity": "High",
                        "evidence": sec,
                        "explanation": "Gemini returned non-JSON, fallback applied."
                    }

                violations.append(result)

        self.shared_state["violations"] = violations
        return violations
