# ClauseSense/gemini/prompts/compliance_prompts.py

def build_compliance_prompt(section_text, rule_text, rule_id):
    """
    Builds a structured prompt for the Gemini model to evaluate
    whether a section of a document violates a compliance rule.
    """

    return f"""
You are a compliance evaluation agent. Your job is to determine whether the given
document section adheres to the mentioned compliance rule.

Rule ID: {rule_id}
Policy Rule:
{rule_text}

Document Section:
{section_text}

Your response must be strictly in the following JSON format:

{{
  "rule_id": "{rule_id}",
  "is_compliant": true or false,
  "explanation": "brief explanation",
  "evidence": "the exact sentence or phrase from the document that proves non-compliance. If compliant, return an empty string."
}}
"""
