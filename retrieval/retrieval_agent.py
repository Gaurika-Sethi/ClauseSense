import re

class RetrievalAgent:
    def __init__(self):
        pass

    def find_relevant_rules(self, document_text, policy_rules):
        """
        Returns only the rules that are relevant to the document
        based on keyword matching.

        Parameters:
        document_text (str): Raw extracted text of the uploaded document.
        policy_rules (list): List of rules, where each rule contains fields:
                             {id, category, rule_text, keywords}

        Returns:
        list: Relevant policy rules
        """
        document_text = document_text.lower()
        relevant_rules = []

        for rule in policy_rules:
            keywords = rule.get("keywords", [])
            for keyword in keywords:
                # Match keyword as whole word (avoid matching inside other words)
                pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
                if re.search(pattern, document_text):
                    relevant_rules.append(rule)
                    break  # no need to check remaining keywords for this rule

        return relevant_rules
