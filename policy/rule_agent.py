# policy/rule_agent.py
from .load_policy import read_policy
class PolicyRuleAgent:
    """Phase 2 agent that extracts structured rules from a policy."""

    def __init__(self, shared_state):
        self.shared_state = shared_state

    def process_policy(self, policy_path):
        print(f"[PHASE 2] Processing policy file: {policy_path}")

        raw = read_policy(policy_path)

        # Split rules by common policy formats
        draft_rules = [
            r.strip() for r in raw.split("\n") 
            if r.strip() and len(r.strip()) > 10
        ]

        rules = []
        for idx, rule in enumerate(draft_rules, start=1):
            rules.append({
                "rule_id": f"R{idx}",
                "text": rule
            })

        # Save to shared state
        self.shared_state["policy_rules"] = rules

        print(f"[PHASE 2] Policy parsing complete.")
        print(f" Total rules extracted: {len(rules)}\n")

        return rules
