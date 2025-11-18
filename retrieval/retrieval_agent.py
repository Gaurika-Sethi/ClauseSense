class RetrievalAgent:
    def __init__(self, shared_state):
        self.shared_state = shared_state

    def find_relevant_rules(self):
        if "policy_rules" not in self.shared_state or "extracted_text" not in self.shared_state:
            print("[PHASE 3] Missing input for rule retrieval.")
            return []

        document_text = self.shared_state["extracted_text"].lower()
        rules = self.shared_state["policy_rules"]
        matches = []

        for rule in rules:
            rule_text = rule["text"].lower()

            # fuzzy/simplified matching
            if "phone" in rule_text and any(char.isdigit() for char in document_text):
                matches.append(rule)
            if "password" in rule_text and "password" in document_text:
                matches.append(rule)
            if "encrypted" in rule_text and "encrypt" in document_text:
                matches.append(rule)

        # 🔥 THIS WAS MISSING
        self.shared_state["matched_rules"] = matches

        print(f"[PHASE 3] Retrieval complete — {len(matches)} relevant rule(s) found.")
        return matches
