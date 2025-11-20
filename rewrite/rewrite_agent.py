# rewrite/rewrite_agent.py

from gemini.gemini_client import generate_completion, is_configured
from gemini.prompts.rewrite_prompts import build_rewrite_prompt

class RewriteAgent:
    def __init__(self, shared_state):
        self.shared_state = shared_state

    def generate_rewrites(self, style="moderate"):
        violations = self.shared_state.get("violations", [])
        rewrites = []

        for v in violations:
            original_text = v["section"]
            rule_text = v["rule_text"]
            rule_id = v["rule_id"]

            if is_configured():
                prompt = build_rewrite_prompt(original_text, rule_text, style)
                rewritten = generate_completion(prompt, max_tokens=250)
            else:
                rewritten = (
                    original_text + "\n[Fallback rewrite: make this compliant manually]"
                )

            rewrites.append({
                "rule_id": rule_id,
                "original_text": original_text,
                "rewrite_suggestion": rewritten
            })

        self.shared_state["rewrites"] = rewrites
        return rewrites
