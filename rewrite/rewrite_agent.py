# rewrite/rewrite_agent.py

class RewriteAgent:
    """
    Generates safe rewrite suggestions for violated sections.
    This version is rule-based and simple — Gemini will replace this later.
    """

    def __init__(self, shared_state):
        self.shared_state = shared_state

    def generate_rewrites(self):
        violations = self.shared_state.get("violations", [])
        rewrites = []

        for v in violations:
            rule_id = v["rule_id"]
            evidence = v["evidence"]

            if rule_id == "R1":      # Password rule
                suggestion = (
                    "Remove shared passwords. Replace with: "
                    "\"All passwords are stored securely and never shared publicly.\""
                )

            elif rule_id == "R2":    # Encryption rule
                suggestion = (
                    "Ensure data is encrypted. You can rewrite as: "
                    "\"All client data is encrypted both in transit and at rest.\""
                )

            elif rule_id == "R3":    # Phone numbers rule
                suggestion = (
                    "Remove personal phone numbers. Replace them with anonymized contact info like: "
                    "\"Contact our support team at [official number].\""
                )

            elif rule_id == "R4":    # USB rule
                suggestion = (
                    "Remove mention of USB usage. Replace with compliant text: "
                    "\"External USB storage devices are not permitted on office systems.\""
                )

            else:
                suggestion = "Rewrite needed, but no template available."

            rewrites.append({
                "rule_id": rule_id,
                "original_text": evidence,
                "rewrite_suggestion": suggestion
            })

        self.shared_state["rewrites"] = rewrites
        return rewrites