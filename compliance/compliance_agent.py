class ComplianceAgent:
    def __init__(self, shared_state):
        self.shared_state = shared_state

    def evaluate_compliance(self):
        rules = self.shared_state.get("matched_rules", [])
        sections = self.shared_state.get("sections", [])
        violations = []

        for rule in rules:
            text = rule["text"].lower()

            for sec in sections:
                sec_l = sec.lower()

                if "phone numbers" in text and any(char.isdigit() for char in sec_l):
                    if any(len(num) >= 7 for num in sec_l.split() if num.isdigit()):
                        violations.append({
                            "rule_id": rule["rule_id"],
                            "rule_text": rule["text"],
                            "evidence": sec.strip(),
                            "severity": "High"
                        })

                if "password" in text and "password" in sec_l:
                    violations.append({
                        "rule_id": rule["rule_id"],
                        "rule_text": rule["text"],
                        "evidence": sec.strip(),
                        "severity": "High"
                    })

        self.shared_state["violations"] = violations
        return violations
