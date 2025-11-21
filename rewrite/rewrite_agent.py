# rewrite/rewrite_agent.py

import google.generativeai as genai
from gemini.prompts.rewrite_prompts import build_rewrite_prompt


class RewriteAgent:
    def __init__(self, state):
        self.state = state

        config = self.state.get("config", {})
        api_key = config.get("GEMINI_API_KEY")
        model = config.get("MODEL")

        if not api_key or not model:
            raise ValueError("Gemini API key or model is missing in shared state config.")

        # Configure Gemini
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)

    def generate_rewrites(self):
        violations = self.state.get("violations", [])
        rewrite_suggestions = []

        for v in violations:
            if not isinstance(v, dict):
                print(f"[REWRITE] ❌ Skipped → Non-dict violation record: {v}")
                continue

            rule_id = v.get("rule_id")
            evidence = v.get("evidence")
            rule_text = v.get("rule_text")
            severity = v.get("severity", "Compliant")

            # only rewrite real violations
            if severity.lower() != "compliant":
                rewrite_suggestions.append({
                    "rule_id": rule_id,
                    "original": evidence,
                    "rule_text": rule_text,
                    "rewrite": f"[Remove or redact confidential information from: '{evidence}']"
                })

        self.state["rewrite_suggestions"] = rewrite_suggestions
        return rewrite_suggestions


