# compliance/compliance_agent.py

import json
from gemini.gemini_client import generate_completion, is_configured
from gemini.prompts.compliance_prompts import build_compliance_prompt
from gemini.utils import parse_json_safe


SEVERITY_PROMPT_TEMPLATE = """
You are an AI compliance auditor.

Given a policy rule violation, classify the severity as:
- LOW: Minor issue, unclear language, small deviation.
- MEDIUM: Meaningful violation but not dangerous.
- HIGH: Serious compliance failure, misleading, harmful, or high-risk.

Return JSON ONLY in this format:
{{
  "severity": "Low | Medium | High",
  "reason": "Short explanation."
}}

--- RULE ---
{rule_text}

--- DOCUMENT SECTION ---
{section}

--- EXPLANATION ---
{explanation}
"""



def classify_severity(rule_text: str, section: str, explanation: str) -> dict:
    """
    Ask Gemini to classify severity.
    """

    prompt = SEVERITY_PROMPT_TEMPLATE.format(
        rule_text=rule_text,
        section=section,
        explanation=explanation
    )

    raw = generate_completion(prompt)

    result = parse_json_safe(raw)

    if not isinstance(result, dict):
        return {
            "severity": "Medium",
            "reason": "Fallback: Gemini returned invalid JSON."
        }

    # Ensure required fields
    result.setdefault("severity", "Medium")
    result.setdefault("reason", "No reason provided.")

    return result



class ComplianceAgent:
    def __init__(self, shared_state):
        self.shared_state = shared_state

    def evaluate_compliance(self):
        violations = []

        matched_rules = self.shared_state.get("matched_rules", [])
        sections = self.shared_state.get("sections", [])

        for rule in matched_rules:
            for sec in sections:

                # 1️⃣ Evaluate rule vs section
                try:
                    prompt = build_compliance_prompt(rule["text"], sec)
                    raw_output = generate_completion(prompt)

                    result = parse_json_safe(raw_output)

                    if not isinstance(result, dict):
                        raise ValueError("Gemini returned non-JSON")

                    # Defaults
                    result.setdefault("rule_id", rule["rule_id"])
                    result.setdefault("rule_text", rule["text"])
                    result.setdefault("section", sec)
                    result.setdefault("status", "Violation")
                    result.setdefault("explanation", "(not provided)")
                    result.setdefault("evidence", sec)

                except Exception:
                    result = {
                        "rule_id": rule["rule_id"],
                        "rule_text": rule["text"],
                        "section": sec,
                        "status": "Violation",
                        "explanation": "Gemini returned non-JSON, fallback applied.",
                        "evidence": sec
                    }

                # 2️⃣ Severity Classification
                sev = classify_severity(
                    rule_text=rule["text"],
                    section=sec,
                    explanation=result.get("explanation", "")
                )

                result["severity"] = sev["severity"]
                result["severity_reason"] = sev["reason"]

                violations.append(result)

        self.shared_state["violations"] = violations
        return violations
