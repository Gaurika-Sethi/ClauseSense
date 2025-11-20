# compliance/compliance_agent.py

import json
from gemini.gemini_client import generate_completion, is_configured
from gemini.prompts.compliance_prompts import build_compliance_prompt

class ComplianceAgent:
    def __init__(self, shared_state):
        self.shared_state = shared_state

    def evaluate_compliance(self):
        rules = self.shared_state.get("matched_rules", [])
        sections = self.shared_state.get("sections", [])
        results = []

        for rule in rules:
            rule_id = rule.get("rule_id")
            rule_text = rule.get("text", "")

            for sec in sections:
                sec_text = sec.strip()

                if is_configured():
                    prompt = build_compliance_prompt(sec_text, rule_text, rule_id)
                    response = generate_completion(prompt, max_tokens=300)

                    try:
                        parsed = json.loads(response)
                        status = parsed.get("status", "Partial")
                        severity = parsed.get("severity", "Medium")
                        explanation = parsed.get("explanation", "")
                    except:
                        status = "Partial"
                        severity = "Low"
                        explanation = "Gemini returned non-JSON, fallback applied."
                else:
                    # fallback logic (when no API key)
                    status = "Partial"
                    severity = "Low"
                    explanation = "Gemini disabled — fallback heuristic."

                # Only record violations or partial matches
                if status in ["Violation", "Partial"]:
                    results.append({
                        "rule_id": rule_id,
                        "rule_text": rule_text,
                        "section": sec_text,
                        "status": status,
                        "severity": severity,
                        "explanation": explanation
                    })

        self.shared_state["violations"] = results
        return results

